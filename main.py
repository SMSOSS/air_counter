#Libraries
import RPi.GPIO as GPIO
import time
from gpiozero import MotionSensor
import dbutil
import credutil

# Change this according to bin max cap
MaxCap =  30

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# PIN Setup
usTrigger = 18
usEcho = 24
movDetect = MotionSensor(4)
 
#set GPIO direction (IN / OUT)
GPIO.setup(usTrigger, GPIO.OUT)
GPIO.setup(usEcho, GPIO.IN)
 
def getDistance():
    GPIO.output(usTrigger, True)
    time.sleep(0.00001)
    GPIO.output(usTrigger, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(usEcho) == 0:
        StartTime = time.time()

    while GPIO.input(usEcho) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    usedCap = (MaxCap - distance) / MaxCap * 100 
 
    return usedCap

def getLastData:
    dbutil.connect()
    query = ("SELECT count, usedcap FROM ({}) WHERE binid=({}) ORDER BY timestamp DESC")
    result = dbutil.read(dbutil.connection, query)
    for r in result:
        curCount = r[0] + 1
        prevCap = r[1]
    

def updateData:
    dbutil.connect()
    getLastData()
    curTS = int(datetime.datetime.now().timestamp()) # current timestamp
    curCap = getDistance()
    table = credutil.db_table
    binid = credutil.db_binid
    if (prevCap - 50 > curCap):
        curCount = 1
    query = ("INSERT INTO ({}) (binid, timestamp, count, usedcap) VALUES =(({}) ({}) ({}) ({}))".format(table, binid, curTS, curCount, curCap))
    dbutil.update(dbutil.connection, query)
    if (credutil.DEBUG == "True"):
        print("[DEBUG] BinValue Update: binid = {} | timestamp = {} | count = {} | capacity = {}% ",format(binid, curTS, curCount, curCap))


if __name__ == '__main__':
    try:
        while True:
            pir.wait_for_motion()
            updateData()
            pir.wait_for_no_motion()

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("[FATAL] KeyboardInterrupt ")
        GPIO.cleanup()