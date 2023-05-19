from fastapi import FastAPI
from config import WEB_CONFIG
from sql_init import sql_init
from swap import BACKGROUND_QUEUE

from asyncio import BaseEventLoop, new_event_loop, run, set_event_loop
from os import getenv, getpid
from os.path import isfile

from dotenv import load_dotenv
from uvicorn import Config, Server

if isfile(".env"):
    load_dotenv(".env")
DEBUG = getenv("DEBUG", False)
if type(DEBUG) != bool:
    DEBUG = DEBUG.lower() == "true"
print(f"DEBUG: {DEBUG}")

app = FastAPI()


@app.get("/")
async def hello():
    return "Hello"


async def main(loop: BaseEventLoop):
    await sql_init()

    config = Config(
        app=app,
        host=WEB_CONFIG.host,
        port=WEB_CONFIG.port,
        loop=loop
    )
    server = Server(config)
    await server.serve()

    loop.stop()

if __name__ == "__main__":
    with open("PID", mode="w") as pid_file:
        pid_file.write(str(getpid()))

    from platform import system
    if system() == "Windows":
        from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    loop = new_event_loop()
    set_event_loop(loop)

    BACKGROUND_QUEUE.start(loop)

    loop.create_task(main(loop))
    loop.run_forever()
