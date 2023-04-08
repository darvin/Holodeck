from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Response

import os
# from fastapi_sqlalchemy import DBSessionMiddleware, db
from holodeck.models import *
# from sqlalchemy.orm import joinedload
from sqlmodel import Field, Session, SQLModel, create_engine, select
from holodeck.gpt_image import generate_image


app = FastAPI()
# app.add_middleware(DBSessionMiddleware, db_url="sqlite+pysqlite:///.data/locations.db") #os.environ['DATABASE_URL'])


sqlite_url = "sqlite+pysqlite:///.data/locations.db"



connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def route_root():
    return {"message": "this is game api"}

@app.get("/location")
async def locations():
    with Session(engine) as session:
        locations = session.exec(select(Location)).all()
        return locations


from holodeck.gpt_game_gen import initialize_location
from holodeck.gpt_text import generate_location_and_encounters

import traceback


location_prompts = [
    # "steampunk city with skyscrapers",
    # "cyberpunk village in Japanese rustic style",
    "fantasy dungsseons and dragons",
    "noir city from 1930s",
    # "StarTrek inspired spaceship",
    # "undeground mine of goblins",
    # "SuperMario style magic land plain",
    # "SuperMario style magic land beach",
]


import concurrent.futures
from tqdm import tqdm

def generate_location(prompt):
    location_dict, encounters_list = generate_location_and_encounters(prompt)
    if location_dict:
        try:
            location = initialize_location(location_dict, encounters_list)
            return location
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()
    else:
        print(f"GENERATING FROM '{prompt}' failed!")
        return None

@app.post("/location")
async def locations_regenerate():
    locations = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(tqdm(executor.map(generate_location, location_prompts), total=len(location_prompts), desc="Generating locations"))
        locations += [r for r in results if r is not None]

    with Session(engine) as session:
        for location in locations:
            session.add(location)
        session.commit()
        for location in locations:
            session.refresh(location)
        return(locations)



from holodeck.gpt_text import \
        generate_object_image_prompt, \
        generate_building_image_prompt, \
        generate_location_image_prompt

import PIL.Image as Image
 

async def generate_image_from_model_and_save(image_model):
    print(f">> requesting image for prompt: '{image_model.prompt}'<<<")
    image_bytes = await generate_image(prompt=image_model.prompt)
    print(">> received image!")
    image = Image.open(image_bytes)
    image_file_name = f".images/{image_model.id}.png"
    image.save(image_file_name)
    image.close()
    image_bytes.close()
    del image_bytes
    return image_model

import asyncio

@app.post("/image/images")
async def image_images_regenerate():
    with Session(engine) as session:
        images = session.exec(select(GameObjectImage).where(GameObjectImage.generated==False)).all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = await asyncio.gather(*[
                generate_image_from_model_and_save(image) 
                for image in images
            ])

            images_generated = [r for r in results if r is not None]
            with Session(engine) as session:
                for image in images_generated:
                    image.generated = True
                    session.add(image)
                session.commit()
                for image in images_generated:
                    session.refresh(image)
                return(images_generated)


@app.post("/image/prompts")
async def image_prompts_regenerate():
    with Session(engine) as session:

        locations = session.exec(select(Location)).all()
        characters = session.exec(select(Character)).all()
        buildings = session.exec(select(Building)).all()

        locations_image_prompts = []
        objects_image_prompts = []
        buildings_image_prompts = []

        def generate_location_images(location):
            return [(location, generate_location_image_prompt(location))]

        def generate_object_images(location):
            prompts = []
            for o in location.objects:
                prompts.append((o, generate_object_image_prompt(o, location)))
            return prompts

        def generate_building_images(location):
            prompts = []
            for b in location.all_buildings:
                prompts.append((b, generate_building_image_prompt(b, location)))
            return prompts

        with concurrent.futures.ThreadPoolExecutor() as executor:
            location_image_futures = [executor.submit(generate_location_images, location) for location in locations if location.image == None]
            object_image_futures = [executor.submit(generate_object_images, character.location) for character in characters if character.location and character.image == None]
            building_image_futures = [executor.submit(generate_building_images, building.location) for building in buildings  if building.location and building.image == None]

            for f in location_image_futures:
                for prompt in f.result():
                    locations_image_prompts.append(prompt)
            for f in object_image_futures:
                for prompt in f.result():
                    objects_image_prompts.append(prompt)
            for f in building_image_futures:
                for prompt in f.result():
                    buildings_image_prompts.append(prompt)


        img_prompts = locations_image_prompts + objects_image_prompts + buildings_image_prompts

        result = []
        for obj, prompt_txt in img_prompts:
            img = GameObjectImage(prompt=prompt_txt)
            obj.image = img
            session.add(img)
            session.add(obj)
            result.append((obj,img))
        session.commit()
        for obj, img in result:
            session.refresh(img)
            session.refresh(obj)
        return result






@app.get("/location/{id}")
async def location(id):
    with Session(engine) as session:

        location = session.exec(select(Location).where(Location.id ==id)).all()[0]
        characters = session.exec(select(Character).where(Character.location_id ==id)).all()
        buildings = session.exec(select(Building).where(Building.location_id ==id)).all()
        ways_outgoing = session.exec(select(Way).where(Way.from_location_id ==id)).all()

        # for way in ways_outgoing:
        #     if way.to_location == None:
        #         way.to_location = generate_location(f"{way.name}: {way.description}. (this location is connected to {location.description})")
        #         session.add(way.to_location)
        #         session.add(way)
        #         session.commit()
        #         session.refresh(location)
        #         await image_prompts_regenerate()
        #         await image_images_regenerate()

        return {
            'location':location,
            'characters':characters,
            'buildings':buildings
        }


@app.get("/character/{id}")
async def character(id):
    with Session(engine) as session:

        character = session.exec(select(Character).where(Character.id ==id)).all()[0]
        if not character.location:
            location = session.exec(select(Location).where(Location.id ==1)).all()[0]
            character.location = location
            session.add(character)
            session.commit()
            session.refresh(character)


        if not character.game_character:
            pass

        if not character.game_items:
            pass

        items = session.exec(select(GameItem).where(GameItem.character_id ==id)).all()

        return {
            'character':character,
            'items':items,
        }

@app.post("/character/{id}/action")
async def character(id):
    with Session(engine) as session:
        character = session.exec(select(Character).where(Character.id ==id)).all()[0]





# To run locally
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)