from datetime import datetime
import time
optionsquareoffH = 15
optionsquareoffM = 31
hour = abs(optionsquareoffH-5)
if optionsquareoffM < 30:
    minutes = optionsquareoffM+30
    hour = abs(optionsquareoffH-6)
else:
    minutes = abs(optionsquareoffM - 30)
now = datetime.now()
print(minutes)
print(hour)
currentTime = now.hour *3600 + now.minute * 60 +now.second + now.microsecond * 0.000001
targetTime = hour*3600 + minutes *60 + 0
print(targetTime)
print(currentTime)
if targetTime < currentTime:
    print("TIME AYIPOYINDI BABOOOIIIIII.............")
    runtime = targetTime

else:
    waittime = targetTime - currentTime
    print("INKA TIME AVVALE MOWAA WAIT SESTUNNNAAA...............")
    # print (waittime)
    time.sleep(waittime+2)
    now = datetime.now()
    print("TIME AYIPOYINDI MOWAAAAAAAAAAAAAAAAAAAAAA.............")