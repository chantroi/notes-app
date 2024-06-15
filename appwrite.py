import subprocess


def main(ctx):
    file = ctx.req.query.get("file")
    with open(f"src/{file}", "r") as f:
        return ctx.res.send(f.read(), 200, {"content-type": "text/plain"})
