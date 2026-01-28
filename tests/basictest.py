from basicprogressbar import BasicProgressBar
import time

prog = BasicProgressBar(1,10,pretext="Before bar:")
for i in range(11):
    time.sleep(0.1)
    prog.current = i
    prog.endtext = (f"I ended on {i}")
    prog.bar(True)

for i in range(11):
    time.sleep(0.1)
    BasicProgressBar(i,10).bar(True)

prog = BasicProgressBar(1,10)
for i in range(11):
    time.sleep(0.1)
    prog.current = i
    prog.posttext = f"processing {i}"
    print(prog.bar(),end=prog.endline)

prog = BasicProgressBar()
for i in range(10):
    time.sleep(0.1)
    print(prog.next(),end="\r")
print()