from sql_init import sql_init

from asyncio import run
from os import getenv, getpid
from os.path import isfile

from dotenv import load_dotenv

if isfile(".env"):
    load_dotenv(".env")
DEBUG = getenv("DEBUG", False)
if type(DEBUG) != bool:
    DEBUG = DEBUG.lower() == "true"
print(f"DEBUG: {DEBUG}")

async def main():
    from anime import Myself
    from time import time
    timer = time()
    for _ in range(3):
        # res = await Myself.get_yearly_data(update=True)
        # res = await Myself.get_weekly_update(update=True)
        pass
    print(time() - timer)
    timer = time()
    for _ in range(1):
        res = await Myself.get_yearly_data(update=None)
        # res = await Myself.get_weekly_update(update=None)
    # print(res["202301"][0].dict())
    print(time() - timer)
    timer = time()
    print(await Myself.get(res["202301"][0].url))
    print(time() - timer)

if __name__ == "__main__":
    with open("PID", mode="w") as pid_file:
        pid_file.write(str(getpid()))

    from platform import system
    if system() == "Windows":
        from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    run(sql_init())

    run(main())
