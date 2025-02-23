import collections
import csv
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> Any:
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/playlists/{name}")
async def get_playlist_data(name: str) -> Any:
    data = collections.defaultdict(list)

    with open("../data/clean/bestest_2025-02-21T14:26:37.csv") as f_in:
        for row in csv.DictReader(f_in):
            data["release_years"].append(int(row["release_date"][:4]))
            data["popularity"].append(int(row["popularity"]))

    return data
