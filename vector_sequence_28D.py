#  Shamelessly stolen from original
#  Posted 23AUG2020 by "gordon77" at
#  https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=282977&p=1717383#p1717383
#  
#  08JAN2021  Attempt to add file read function to "vector_sequence_14.py"
#  11JAN2021  Attempting to add nested FOR loop for applying test vectors ("vector_sequence_19.py")


#!/usr/bin/env python3
from multiprocessing import Process
import time
import RPi.GPIO as GPIO
import guizero
from guizero import App, PushButton, Text, TextBox
from array import *


# Pin definitions
SIG1_pin = 17
SIG2_pin = 18
SIG3_pin = 27

# Suppress warnings
GPIO.setwarnings(False)

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

# Set both pins as outputs
GPIO.setup(SIG1_pin, GPIO.OUT)
GPIO.setup(SIG2_pin, GPIO.OUT)
GPIO.setup(SIG3_pin, GPIO.OUT)

class button:
    def __init__(self,index,image,grid):
        self.index = index
        self.image = image
        self.grid  = grid


def Flasher1On():
    global freq1,duty1,jobs1,tbvalue,p1,sig1status
    for i in jobs1:
        i.terminate()
    jobs1=[]
    flasher1ontxt = Text(app, text=" RUNNING  ", grid=[1,0])
    time1on  = tbvalue
    time1off = tbvalue
    p1 = Process(target=togSigOne,args = (time1on,time1off))
    p1.start()
    jobs1.append(p1)
    sig1status = True

def Flasher2On():
    global freq2,duty2,jobs2,tbvalue,p2,sig2status
    for i in jobs2:
        i.terminate()
    jobs2=[]
    flasher2ontxt = Text(app, text=" RUNNING  ", grid=[1,2])
    time2on  = tbvalue
    time2off = tbvalue
    p2 = Process(target=togSlowSigs)
    p2.start()
    jobs2.append(p2)
    sig2status = True

def Flasher1Off():
    global time1on,time1off,jobs1,SIG1_pin,sig1status
    flasher1ontxt = Text(app, text=" STOPPED  ", grid=[1,0])
    for i in jobs1:
        i.terminate()
    jobs1=[]
    GPIO.output(SIG1_pin, GPIO.LOW)
    sig1status = False

def Flasher2Off():
    global time2on,time2off,jobs2,SIG2_pin,sig2status
    flasher2ontxt = Text(app, text=" STOPPED  ", grid=[1,2])
    for i in jobs2:
        i.terminate()
    jobs2=[]
    GPIO.output(SIG2_pin, GPIO.LOW)
    sig2status = False

def Exit():
    global jobs1,jobs2,SIG1_pin,SIG2_pin
    for i in jobs1:
        i.terminate()
    for i in jobs2:
        i.terminate()
    GPIO.output(SIG1_pin, GPIO.LOW)
    GPIO.output(SIG2_pin, GPIO.LOW)
    exit()

# Define a function apply the Test Vectors
def togSigOne(time1on,time1off):
    while True:
        GPIO.output(SIG1_pin, GPIO.HIGH)  # Sig #1 ON     #############################################
        time.sleep(time1on)                               # This entire section will be replaced when  
        GPIO.output(SIG1_pin, GPIO.LOW)   # Sig #1 OFF    # we get routine working to read vectors from
        time.sleep(time1off)                              # file and convert to signal transitions     

# Define a function apply the Test Vectors for Signals 2 thru 4
# def togSigTwo(time2on,time2off):
def togSlowSigs():
#    while True:

#        GPIO.output(SIG2_pin, GPIO.HIGH)  # Sig #2 ON     #############################################
#        time.sleep(time2on)                               # This entire section will be replaced when  
#        GPIO.output(SIG2_pin, GPIO.LOW)   # Sig #2 OFF    # we get routine working to read vectors from
#        time.sleep(time2off)                              # file and convert to signal transitions     
#    global tbvalue
    vectors = [[1, 2],
               [1, 2],
               [1, 3],
               [1, 3],
               [1, 2],
               [3, 2]]  # [time delay multiplier, Signal Number]
    numVectorRows = 6
    numVectorClms = 2
    curSigState = [0, 0, 0]
    outSigPinNum = [17, 18, 27]
    stdDelay = 0.200
    
    while True:                                      # remove this 'while' for single iteration (each vector executed only once)
        for rowIndex in range(0, numVectorRows):
            sigPinIndex = vectors[rowIndex][1] - 1    # equal to (Signal Number) - 1
            GPIO.output(outSigPinNum[sigPinIndex], not curSigState[sigPinIndex])
            curSigState[sigPinIndex] = not curSigState[sigPinIndex]
            time.sleep((vectors[rowIndex][0]) * stdDelay ) 




# Define a function to change the Timebase
def ChangeTimeBase():
    global tbvalue, sig1status, sig2status
    print("ChangeTimeBase() has been called")
    tbvalue = float( timebase.value )
    print("New Timebase is" , tbvalue)
    if (sig1status == True):
        Flasher1Off()
        Flasher1On()
    if (sig2status == True):
        Flasher2Off()
        Flasher2On()
    
# Define a function to read the Test Vector File
def ReadVectorFile():
    global vectorfilename
    print("ReadVectorFile() has been called")
    print("New File is" , vectorfilename.value)
    


###########
# GUI Stuff
###########

sig1onbtn       = button(0,  '1_ON'   ,[0,0])
sig1offbtn      = button(1,  '1_OFF'  ,[0,1])
sig2onbtn       = button(2,  '2_ON'   ,[0,2])
sig2offbtn      = button(3,  '2_OFF'  ,[0,3])
changetbbtn     = button(4,  'CH_TB'  ,[0,4])
exitbtn         = button(5,  'EXIT'   ,[1,5])

app = App(title="Machine Signal Simulator", width=350, height=350, layout="grid")

sig1onbtn       = PushButton(app, command=Flasher1On,     text = "CH1 ON",   grid=sig1onbtn.grid)
sig1offbtn      = PushButton(app, command=Flasher1Off,    text = "CH1 OFF",  grid=sig1offbtn.grid)
sig2onbtn       = PushButton(app, command=Flasher2On,     text = "CH2 ON",   grid=sig2onbtn.grid)
sig2offbtn      = PushButton(app, command=Flasher2Off,    text = "CH2 OFF",  grid=sig2offbtn.grid)
changetbbtn     = PushButton(app, command=ChangeTimeBase, text = "CH TB",    grid=changetbbtn.grid) 
exitbtn         = PushButton(app, command=Exit,           text = "EXIT",     grid=exitbtn.grid)

timebase_label =    Text(app, text="NewTimebase:  ", grid=[1,4], align="left")
timebase       = TextBox(app,                        grid=[2,4], align="left", width=10)

#   vectorfilename_label = Text(app, text="Vector File:  ", grid=[0,5], align="left")
#   vectorfilename       = TextBox(app, grid=[1,5], align="left", width=25)



def main():
    global jobs1, jobs2, tbvalue
    tbvalue = 0.125         # In case user clicks "ON" button before clicking "CH TB" button
    jobs1=[]               # (in which case tbvalue would not have been assigned)
    jobs2=[]
    app.display()
    while True:
        time.sleep(0.1)

if __name__ == '__main__':
    main()