from fastapi import FastAPI, WebSocket, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from data import Note
import names
import json
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")
notes = Note()

def sanitize(input_string):
    sanitized_string = re.sub(r'[^a-zA-Z0-9_]', '', input_string)
    sanitized_string = sanitized_string.lstrip('_')
    return sanitized_string
    
def extract_raw(input_string):
    start_index = input_string.find("<pre>")
    end_index = input_string.find("</pre>")
    if start_index != -1 and end_index != -1:
        content = input_string[start_index + len("<pre>"):end_index]
        return content
    else:
        return None

@app.get("/")
async def home():
    note_name = names.get_first_name(gender='female').lower()
    return RedirectResponse("/{}/edit".format(note_name))
    
@app.get("/{note_name}/edit")
async def note_editor(request: Request, note_name: str):
    user_agent = request.headers.get("user-agent")
    try:
        content = notes.get_note(note_name)
    except Exception as e:
        print(e)
        content = ""
    if "Mozilla" in user_agent:
        hostname = request.url.hostname
        ws_url = "wss://{}/ws".format(hostname)
        print(ws_url)
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
        if "<pre>" in content and "</pre>" in content:
            content = extract_raw(content)
        return Response(
            content, 
            media_type="text/plain"
            )
            
@app.get("/{note_name}")
async def render_note(request: Request, note_name: str):
    user_agent = request.headers.get("user-agent")
    try:
        content = notes.get_note(note_name)
    except Exception as e:
        print(e)
        content = ""
    if "Mozilla" in user_agent:
        with open("btn.html", "r") as f:
            content = content + f.read()
        if "</" in content:
            return HTMLResponse(content)
        else:
            return Response(
            content, 
            media_type="text/plain"
            )
    else:
        if "<pre>" in content and "</pre>" in content:
            content = extract_raw(content)
        return Response(
            content, 
            media_type="text/plain"
            )
    
@app.websocket("/ws")
async def write_note(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        data = data.split(":=:")
        note_name = sanitize(data[0])
        content = data[1]
        print(note_name)
        try:
            notes.add_note(note_name, content)
        except Exception as e:
            print(e)
            notes.update_note(note_name, content)
        #await ws.send_text(content)