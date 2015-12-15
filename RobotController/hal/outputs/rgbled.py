#!/usr/bin/python
from time import sleep
import RPi.GPIO as GPIO

#Common Cathode RGB-LEDs (Cathode=Active Low)
RGB_ENABLE = 0
RGB_DISABLE = 1

#LED CONFIG - Set GPIO Ports
RGB_RED = 18
RGB_GREEN = 23
RGB_BLUE = 24
RGB_CYAN = [RGB_GREEN,RGB_BLUE]
RGB_MAGENTA = [RGB_RED,RGB_BLUE]
RGB_YELLOW = [RGB_RED,RGB_GREEN]
RGB_WHITE = [RGB_RED,RGB_GREEN,RGB_BLUE]

RGB = [RGB_RED,RGB_GREEN,RGB_BLUE]
RGB_LIST = [RGB_RED,RGB_GREEN,RGB_BLUE,RGB_CYAN,RGB_MAGENTA,RGB_YELLOW,RGB_WHITE]

def ledSetup():
  #Set up the wiring
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  # Setup Ports
  for val in RGB:
    GPIO.setup(val, GPIO.OUT)
  ledClear()

def setColor(color):
  ledClear()
  if isinstance(color,int):
    GPIO.output(color, RGB_ENABLE)
  else:
    for c in color:
      GPIO.output(c, RGB_ENABLE)

def ledClear():
  for val in RGB:
    GPIO.output(val, RGB_DISABLE)

def ledCleanup():
  ledClear()
  GPIO.cleanup(RGB)

def main():
  ledSetup()
  for num in range(0,5):
    setColor(RGB_RED)
    sleep(1)
    setColor(RGB_GREEN)
    sleep(1)
    setColor(RGB_BLUE)
    sleep(1)
    setColor(RGB_CYAN)
    sleep(1)
    setColor(RGB_MAGENTA)
    sleep(1)
    setColor(RGB_YELLOW)
    sleep(1)
  ledCleanup()

# Test harnesses 
if __name__=='__main__':
  main()
#End
