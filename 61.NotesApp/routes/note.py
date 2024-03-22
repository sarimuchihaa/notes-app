from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from config.db import conn
from fastapi.templating import Jinja2Templates
from schemas.note import noteEntity, notesEntity

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        try:
            newDocs.append({
                "id": doc["_id"],
                "title": doc["title"],
                "desc": doc["desc"],
                "important": doc["important"],
            })
        except KeyError:
            # Handle missing 'note' key here, for example, by skipping this document
            pass
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


@note.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    note = conn.notes.notes.insert_one(formDict)
    return {"Success": True}
