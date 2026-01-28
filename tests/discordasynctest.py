import basicprogressbar
import asyncio

distoken = input("Please input a discord token\n")

totals = 50
dis = basicprogressbar.DiscordProgressBarAsync(0.0,totals, idtoken=distoken,throttle=2,length = 40)

async def sending():
    for i in range(1,51):
        dis.current = i
        await dis.send()
        await asyncio.sleep(1)

asyncio.run(sending())