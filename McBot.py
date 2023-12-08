# %% Import libraries used
import keyboard
import pandas as pd
from PIL import ImageGrab
import numpy as np
import mouse
import pyautogui
import cv2
import time
from pynput import mouse
import win32api
import threading
# %% Define all Variables
timestamps = []
screenshots = []
InputArrays = []
LeftClicked = 0
RightClicked = 0
ScrollingUp = 0
ScrollingDown = 0
ScrollingUp = 0
ScrollingDown = 0
# %% Define all functions
def On_scroll(x, y, dx, dy):
    global ScrollingUp, ScrollingDown

    ScrollingUp = 1 if dy > 0 else 0
    ScrollingDown = 1 if dy < 0 else 0

def GetInputArray():
    
    InputArray = np.zeros((25, 1))
    
    # Record keyboard inputs
    if keyboard.is_pressed('w'):
        InputArray[0] = 1
    if keyboard.is_pressed('a'):
        InputArray[1] = 1
    if keyboard.is_pressed('s'):
        InputArray[2] = 1
    if keyboard.is_pressed('d'):
        InputArray[3] = 1
    if keyboard.is_pressed('e'):
        InputArray[4] = 1
    if keyboard.is_pressed('q'):
        InputArray[5] = 1
    if keyboard.is_pressed('space'):
        InputArray[6] = 1
    if keyboard.is_pressed('shift'):
        InputArray[7] = 1
    if keyboard.is_pressed('strg'):
        InputArray[8] = 1
    if keyboard.is_pressed('1'):
        InputArray[9] = 1
    if keyboard.is_pressed('2'):
        InputArray[10] = 1
    if keyboard.is_pressed('3'):
        InputArray[11] = 1
    if keyboard.is_pressed('4'):
        InputArray[12] = 1
    if keyboard.is_pressed('5'):
        InputArray[13] = 1
    if keyboard.is_pressed('6'):
        InputArray[14] = 1
    if keyboard.is_pressed('7'):
        InputArray[15] = 1
    if keyboard.is_pressed('8'):
        InputArray[16] = 1
    if keyboard.is_pressed('9'):
        InputArray[17] = 1
    if keyboard.is_pressed('0'):
        InputArray[18] = 1
    InputArray[19] = int(win32api.GetAsyncKeyState(0x01) == -32767)
    InputArray[20] = int(win32api.GetAsyncKeyState(0x02) == -32767)
    InputArray[21] = ScrollingUp
    InputArray[22] = ScrollingDown
    InputArray[23] = pyautogui.position()[0]
    InputArray[24] = pyautogui.position()[1]
    
    return InputArray

def GatherData():
    listener = mouse.Listener(on_scroll=On_scroll)
    listener.start()
    
    while True:
        # Capture screenshot
        screenshot = ImageGrab.grab()
        screenshots.append(np.array(screenshot))

        # Record timestamp
        timestamp = pd.Timestamp.now()
        timestamps.append(timestamp)
        
        InputArrays.append(GetInputArray())

        # Check for program termination
        if keyboard.is_pressed('-'):
            break
            listener.stop()
            
        time.sleep(0.07)
        
    return screenshots, timestamps, InputArrays

def ShowImage(Image):
    cv2.imshow("Zeros matx", Image) # show numpy array
     
    cv2.waitKey(0) # wait for ay key to exit window
    cv2.destroyAllWindows() # close all windows
# %% Gather The Data we need
screenshots, timestamps, InputArrays = GatherData()
data = {'Timestamps': timestamps, 'Screenshots': screenshots, 'Keyboard Inputs': InputArrays}
df = pd.DataFrame(data)
df.to_csv('ISC_Data')
# %%