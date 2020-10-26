import time
import os

pid = os.getgid() #process indetifier

while True:
    print(pid, time.time())
    time.sleep(2)