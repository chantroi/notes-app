from fastapi import FastAPI, WebSocket, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from data import Note
import names

app = FastAPI()
templates = Jinja2Templates(directory="templates")
notes = Note()

@app.get("/")
async def home():
    note_name = names.get_first_name(gender='female').lower()
    return RedirectResponse("/{}".format(note_name))
    
@app.get("/{note_name}")
async def note_editor(request: Request, note_name: str):
    user_agent = request.headers.get("user-agent")
    content = notes.get_note(note_name)
    if "Mozilla" in user_agent:
        hostname = request.url.hostname
        ws_url = "wss://{}/ws".format(hostname)
        return templates.TemplateResponse(
            request=request, 
            name="index.html", 
            context={
                "name": note_name,
                "content": content,
                "ws_url": ws_url
                }
            )
    else:
        return Response(
            content, 
            media_type="text/plain"
            )
    
@app.websocket("/ws")
async def write_note(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_json()
        note_name = data.name
        content = data.content
        try:
            notes.add_note(note_name, content)
        except Exception as e:
            print(e)
            notes.update_note(note_name, content)
        await ws.send_text(content)