import subprocess
import os


def main(ctx):
    return ctx.res.json(os.listdir("src"))
