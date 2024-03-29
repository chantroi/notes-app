from flask import Flask, render_template, redirect, request, Response
from data import Note
import names
import json
import re

app = Flask(__name__)
notes = Note()

def sanitize(input_string):
    sanitized_string = re.sub(r'[^a-zA-Z0-9_]', '', input_string)
    sanitized_string = sanitized_string.lstrip('_')
    return sanitized_string
    
def extract_raw(input_string):
    start_index = input_string.find("<code>")
    end_index = input_string.find("</code>")
    if start_index != -1 and end_index != -1:
        content = input_string[start_index + len("<code>"):end_index]
        return content
    else:
        return None

@app.route('/')
def home():
    note_name = names.get_first_name(gender='female').lower()
    return redirect("/{}/edit".format(note_name))
    
@app.route('/<name>/edit')
def edit_note(name):
    user_agent = request.headers.get("user-agent")
    try:
        content = notes.get_note(name)
    except Exception as e:
        print(e)
        content = ""
    if "Mozilla" in user_agent:
        host = request.host
        url = "https://" + host + "/edit"
        return render_template(
            'flask.html', 
            name=name,
            content=content,
            url=url
            )
    else:
        if "<code>" in content and "</code>" in content:
            content = extract_raw(content)
        return Response(
            content, 
            mimetype="text/plain"
            )
            
@app.route('/<name>')
def render_note(name):
    user_agent = request.headers.get("user-agent")
    try:
        content = notes.get_note(name)
    except Exception as e:
        print(e)
        content = ""
    if "Mozilla" in user_agent:
        if "</" not in content:
            content = "<pre><code>" + content + "</code></pre>"
        with open("btn.html", "r") as f:
            html = f.read()
        content = html.replace("{{content}}", content)
        return Response(
            content, 
            mimetype='text/html'
            )
    else:
        if "<code>" in content and "</code>" in content:
            content = extract_raw(content)
        return Response(
            content, 
            mimetype="text/plain"
            )
            
@app.route('/edit', methods=['POST'])
def post_edit():
    data = request.json
    name = data.get('name')
    content = data.get('content')
    try:
        notes.add_note(name, content)
    except Exception as e:
        print(e)
        notes.update_note(name, content)
    return "OK"