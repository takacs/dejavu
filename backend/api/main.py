import sqlite3
from fastapi import FastAPI, Depends
from database.connections import ConnectionManager
import appdirs
from api.models import Severity, Status, TrashType, User, Trash, TrashCreate, Cleaner


app = FastAPI()

# TODO: consts
DATABASE_URL = appdirs.user_data_dir("trashman") + "/trashman.db"

connection_manager = ConnectionManager(DATABASE_URL)


def get_db():
    with connection_manager as db:
        yield db


@app.get("/")
async def root():
    return {"message": "Hello Wold"}


@app.get("/status")
async def get_statuses(db: sqlite3.Connection = Depends(get_db)):
    statuses = [
        Status(id=x[0], name=x[1])
        for x in db.execute("select * from status").fetchall()
    ]
    return {"statuses": statuses}


@app.get("/severity")
async def get_severities(db: sqlite3.Connection = Depends(get_db)):
    severities = [
        Severity(id=x[0], name=x[1])
        for x in db.execute("select * from severity").fetchall()
    ]
    return {"severities": severities}


@app.get("/trash_type")
async def get_trash_types(db: sqlite3.Connection = Depends(get_db)):
    trash_types = [
        TrashType(id=x[0], name=x[1])
        for x in db.execute("select * from trash_type").fetchall()
    ]
    return {"trash_types": trash_types}


@app.get("/user")
async def get_users(db: sqlite3.Connection = Depends(get_db)):
    users = [
        User(id=x[0], username=x[1], email=x[2], user_type_id=x[3])
        for x in db.execute(
            "select id, username, email, user_type_id from user"
        ).fetchall()
    ]
    return {"users": users}


@app.get("/user/{user_id}")
async def get_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    x = db.execute(
        f"select id, username, email, user_type_id from user where id = {user_id}"
    ).fetchone()
    user = User(id=x[0], username=x[1], email=x[2], user_type_id=x[3])
    return {"user": user}


@app.get("/trash")
async def get_trash(db: sqlite3.Connection = Depends(get_db)):
    trash = [
        Trash(
            id=x[0],
            created_by=x[1],
            created_at=x[2],
            cleaned_by=x[3],
            cleaned_at=x[4],
            location_x=x[5],
            location_y=x[6],
            trash_type_id=x[7],
            status_id=x[8],
            severity_id=x[9],
            image_url=x[10],
            description=x[11],
        )
        for x in db.execute(
            """
            select
                id,
                created_by,
                created_at,
                cleaned_by,
                cleaned_at,
                location_x,
                location_y,
                trash_type_id,
                status_id,
                severity_id,
                image_url,
                description
             from trash"""
        ).fetchall()
    ]
    return {"trash": trash}


@app.get("/trash/{trash_id}")
async def get_a_trash(trash_id: int, db: sqlite3.Connection = Depends(get_db)):
    x = db.execute(
        f"""
        select
            id,
            created_by,
            created_at,
            cleaned_by,
            cleaned_at,
            location_x,
            location_y,
            trash_type_id,
            status_id,
            severity_id,
            image_url,
            description
         from trash where id = {trash_id}"""
    ).fetchone()
    trash = Trash(
        id=x[0],
        created_by=x[1],
        created_at=x[2],
        cleaned_by=x[3],
        cleaned_at=x[4],
        location_x=x[5],
        location_y=x[6],
        trash_type_id=x[7],
        status_id=x[8],
        severity_id=x[9],
        image_url=x[10],
        description=x[11],
    )
    return {"trash": trash}


@app.post("/trash")
async def create_trash(trash: TrashCreate, db: sqlite3.Connection = Depends(get_db)):
    query = f"""
        insert into trash
        (created_by, created_at, location_x, location_y,
        trash_type_id, status_id, severity_id, image_url,
        description)
        values
        ("{trash.created_by}", "{trash.created_at}", {trash.location_x},
        {trash.location_y}, {trash.trash_type_id}, {trash.status_id},
        {trash.severity_id}, "{trash.image_url}", "{trash.description}")
        """
    db.execute(query)
    db.commit()
    return {"status": "Success"}


@app.patch("/trash/clean/{trash_id}")
async def clean_trash(
    trash_id: int, cleaner: Cleaner, db: sqlite3.Connection = Depends(get_db)
):
    db.execute(f"""
    update trash
    set
        cleaned_by = "{cleaner.cleaned_by}",
        cleaned_at = "{cleaner.cleaned_at}",
        status_id = 3
    where id = {trash_id}
    """)
    db.commit()
    return {"status": "Success"}


@app.delete("/trash/{trash_id}")
async def delete_trash(trash_id: int, db: sqlite3.Connection = Depends(get_db)):
    query = f"""
    delete from trash
    where id = {trash_id}
    """
    db.execute(query)
    db.commit()
    return {"status": "Success"}
