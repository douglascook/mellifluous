import collections
import pathlib
import sqlite3
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

APP_ROOT = pathlib.Path(__file__).parent
DB_PATH = "./db/mellifluous.sqlite3"

app = FastAPI()
app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")
templates = Jinja2Templates(directory=APP_ROOT / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> Any:
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/playlists/{name}")
async def get_playlist_data(name: str) -> Any:
    data = collections.defaultdict(list)

    with sqlite3.connect(DB_PATH, autocommit=False) as db:
        db.row_factory = sqlite3.Row

        cursor = db.cursor()
        cursor.execute(
            """
            SELECT release_date, popularity
            FROM track
                JOIN playlist ON playlist.id = track.playlist_id
            WHERE playlist.name = ?
            """,
            (name,),
        )
        for row in cursor:
            data["release_years"].append(int(row["release_date"][:4]))
            data["popularity"].append(int(row["popularity"]))

    return data
