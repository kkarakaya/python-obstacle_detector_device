# state_list.py
from state import State
import board
import digitalio
import time
import adafruit_hcsr04
 
ledGreen = digitalio.DigitalInOut(board.D7)
ledYellow = digitalio.DigitalInOut(board.D8)
ledRed = digitalio.DigitalInOut(board.D9)
buzzer = digitalio.DigitalInOut(board.D11)

ledGreen.direction = digitalio.Direction.OUTPUT
ledYellow.direction = digitalio.Direction.OUTPUT
ledRed.direction = digitalio.Direction.OUTPUT
buzzer.direction = digitalio.Direction.OUTPUT

distanceSensor = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D2)

    
class Init_State(State):
    def __init__(self):
        print("“Obstacle Detector Device is Working.")
        ledGreen.value = True
        time.sleep(2)
        ledGreen.value = False
        time.sleep(2) 
        ledYellow.value = True
        time.sleep(2)
        ledYellow.value = False
        time.sleep(2) 
        ledRed.value = True
        time.sleep(2)
        ledRed.value = False
        time.sleep(2) 
        buzzer.value = True
        time.sleep(2)
        buzzer.value = False
    def transition(self):
        dist = distanceSensor.distance()
        if dist < 200 and dist > 120:
            return Second_State()
        elif dist < 120 and dist > 50:
            return Third_State()
        elif dist < 50 and dist > 25:
            return Fourth_State()
        elif dist >= 200:
            return Fifth_State()
        else:
            return Last_State()  
        
class Second_State(State):
    def transition(self):
        dist = distanceSensor.distance()
        if dist < 200 and dist > 120:
            ledGreen.value = True
            ledYellow.value = False
            ledRed.value = False
            buzzer.value = False
            print("You are Safe")
            return self
        elif dist >= 200:
            return Fifth_State()
        else:
            return Third_State()       

class Third_State(State):
    def transition(self):
        dist = distanceSensor.distance()
        if dist < 120 and dist > 50:
            ledGreen.value = False
            ledYellow.value = True
            ledRed.value = False
            buzzer.value = False
            print("Slow Down Your Speed")
            return self
        elif dist >= 120:
            return Second_State()
        else:
            return Fourth_State()  

class Fourth_State(State):
    def transition(self):
        dist = distanceSensor.distance()
        if dist < 50 and dist > 25:
            ledGreen.value = False
            ledYellow.value = False
            ledRed.value = True
            buzzer.value = False            
            print("DANGER TOO CLOSE")
            return self
        elif dist >= 50:
            return Third_State()
        else:
            return Last_State()  

class Fifth_State(State):
    def transition(self):
        dist = distanceSensor.distance()
        if dist >= 200:
            ledGreen.value = True
            ledYellow.value = True
            ledRed.value = False
            buzzer.value = False
            print("Distance Error")
            return self
        else:
            return Second_State()  

class Last_State(State):
    programFinished = 0
    startTime = 0
    currentTime = 0
    is_first = 1
    def transition(self):
        if not self.programFinished:
            dist = distanceSensor.distance()
            if dist <= 25:
                ledGreen.value = False
                ledYellow.value = False
                ledRed.value = True
                buzzer.value = True
                if self.is_first:
                    self.startTime = time.time
                    self.is_first = 0
                else:
                    self.currentTime = time.time
                    if self.currentTime-self.startTime > 5:
                        print("The Device Stopped! Calling the Emergency Services.")
                        self.programFinished = 1
                return self
            else:
                self.startTime = 0
                self.currentTime = 0
                self.is_first = 1
                return Second_State()  

# End of our states.