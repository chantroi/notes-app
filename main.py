from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from db import DB
from util import extract_raw, generate_name

db = DB()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    path = generate_name()
    return RedirectResponse(f"/{path}")


@app.get("/{path}")
def note_route(request: Request, path: str):
    note = db.get(path)
    headers = request.headers
    user_agent = headers.get("User-Agent")
    if note is None:
        content = ""
    else:
        content = note.content
    if "Mozilla" in user_agent:
        return templates.TemplateResponse(
            "index.html", {"request": request, "content": content}
        )
    return Response(extract_raw(content), status_code=200, media_type="text/plain")


@app.post("/{path}")
def note_post(request: Request, path: str):
    data = request.body()
    db.add(path, data)
    return Response(data, status_code=200, media_type="text/plain")
