from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Response

import os
# from fastapi_sqlalchemy import DBSessionMiddleware, db
from holodeck.models.game_objects import *
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





# To run locally
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)