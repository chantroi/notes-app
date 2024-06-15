import re
import names
from .data import Note

notes = Note()


def sanitize(input_string):
    sanitized_string = re.sub(r"[^a-zA-Z0-9_]", "", input_string)
    sanitized_string = sanitized_string.lstrip("_")
    return sanitized_string


def extract_raw(input_string):
    start_index = input_string.find("<code>")
    end_index = input_string.find("</code>")
    if start_index != -1 and end_index != -1:
        content = input_string[start_index + len("<code>") : end_index]
        return content
    else:
        return None


def main(ctx):
    if ctx.req.method == "POST" and ctx.req.path == "/edit":
        data = ctx.req.body
        name = data.get("name")
        content = data.get("content")
        try:
            notes.add_note(name, content)
        except Exception as e:
            print(e)
            notes.update_note(name, content)
        return ctx.res.send(content, 200, dict(content_type="text/plain"))
    if ctx.req.path == "/":
        note_name = names.get_first_name(gender="female").lower()
        return ctx.res.redirect("/{}".format(note_name))

    user_agent = ctx.req.headers.get("user-agent")
    mode = ctx.req.query.get("mode")
    name = ctx.req.path.replace("/", "")
    try:
        content = notes.get_note(name)
    except Exception as e:
        print(e)
        content = ""
    if mode == "view":
        if "<code>" not in content:
            content = "<pre><code>" + content + "</code></pre>"
        html = open("src/function/templates/htmx/view.html", "r").read()
        html = html.replace("{{ content | safe }}", content)
        return ctx.res.send(html, 200, {"content-type": "text/html"})
    elif mode == "edit":
        html = open("src/function/templates/htmx/edit.html", "r").read()
        html = html.replace("{{ content }}", content)
        return ctx.res.send(html, 200, {"content-type": "text/html"})
    if "Mozilla" in user_agent:
        host = ctx.req.host
        post_url = "https://" + host + "/edit"
        self_url = ctx.req.url
        html = open("src/function/templates/index.html", "r").read()
        html = (
            html.replace("{{ content }}", content)
            .replace("{{ post_url }}", post_url)
            .replace("{{ self_url }}", self_url)
        )
        return ctx.res.send(html, 200, {"content-type": "text/html"})
    else:
        if "<code>" in content and "</code>" in content:
            content = extract_raw(content)
        return ctx.res.send(content, 200, {"content-type": "text/plain"})
