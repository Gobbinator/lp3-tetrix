#! /usr/bin/env python3
#a test and protoype for return-less keyboard input
#DROPPED due to bad module support and needing to be executed as root
import keyboard as kb

while True:
    if kb.is_pressed('w'):
        print('W is pressed')
