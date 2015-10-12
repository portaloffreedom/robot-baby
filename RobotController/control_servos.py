#!/usr/bin/python3

import sys
from hal.outputs.servo import Servo

def center_servo(pin):
    s = Servo(pin)
    s.center()
    return s

def off_servo(pin):
    s = Servo(pin)
    s.off()
    return s

def incorrect_usage():
    print("incorrect usage. Proper usage is \"{} [center,off] [list of pins...]".format(sys.argv[0]))
    exit(1)
    

if __name__ == "__main__":
    if len(sys.argv) < 3:
        incorrect_usage()
        
    command = sys.argv[1]
    
    pins = sys.argv[2:]
        
    if command == "center":
        operation = center_servo
    elif command == "off":
        operation = off_servo
    else:
        incorrect_usage()

    for pin in pins:
        operation(int(pin))
        
    exit(0)
    