import basicprogressbar
import time

distoken = input("Please input a discord token\n")

totals = 5000000
dis = basicprogressbar.DiscordProgressBar(
    0.0, totals, idtoken=distoken, throttle=2, length=40, showtimer=True)


def sending():
    for i in range(1, totals+1):
        dis.current = i
        dis.send()
        time.sleep(1)


sending()
