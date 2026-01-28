import basicprogressbar
import time

distoken = input("Please input a discord token\n")

totals = 50
dis = basicprogressbar.DiscordProgressBar(0.0,totals, idtoken=distoken,throttle=2,length = 40)

def sending():
    for i in range(1,51):
        dis.current = i
        dis.send()
        time.sleep(1)

sending()