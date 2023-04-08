from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Response

import os
# from fastapi_sqlalchemy import DBSessionMiddleware, db
from holodeck.models.game_objects import *
from holodeck.models.game_engine import *
# from sqlalchemy.orm import joinedload
from sqlmodel import Field, Session, SQLModel, create_engine, select


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





@app.get("/location/{id}")
async def location(id):
    with Session(engine) as session:

        location = session.exec(select(Location).where(Location.id ==id)).all()[0]
        characters = session.exec(select(Character).where(Character.location_id ==id)).all()
        buildings = session.exec(select(Building).where(Building.location_id ==id)).all()

        return {
            'location':location,
            'characters':characters,
            'buildings':buildings
        }


@app.get("/character/{id}")
async def character(id):
    with Session(engine) as session:

        character = session.exec(select(Character).where(Character.id ==id)).all()[0]

        if not character.game_character:
            pass

        if not character.game_items:
            pass

        items = session.exec(select(GameItem).where(GameItem.character_id ==id)).all()

        return {
            'character':character,
            'items':items,
        }




# To run locally
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)