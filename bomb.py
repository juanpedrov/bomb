#!/usr/bin/env python3
import datetime
import pifacecad
import time
import os
import threading
from pifacecad.tools.question import LCDQuestion

from datetime import timedelta

#--- bomb time in seconds
TIME = 5400

#--- button constants
RED = 0
GREEN = 1
YELLOW = 2
BLUE = 3
RESET = 4

#--- correct sequence
CORRECT_SEQUENCE = [RED, GREEN, YELLOW, BLUE, RED, GREEN, YELLOW, BLUE]


class Bomb(object):
    def __init__(self, cad, bomb_time, correct_sequence):
        self.cad = cad
        self.bomb_time = bomb_time
        self.time_left = bomb_time
        self.correct_sequence = correct_sequence


class BombGame(object):
    def __init__(self, bomb_time, correct_sequence):
        self.cad = pifacecad.PiFaceCAD()         #Init PiFace control and dysplay
        self.bomb = Bomb(self.cad, bomb_time,
                         correct_sequence)       #Init Bomb object
        self.listener = pifacecad.SwitchEventListener(
                chip=self.cad)                   #Register Event Listener
        self.t_chronometer_sound = threading.Thread(target=self.play_chronometer)
        self.t_countdown = threading.Thread(target=self.countdown)
        
    def start(self):
        self.register_button_events()
        
        #Turn on back light
        self.cad.lcd.backlight_on()
        #Turn off cursor and blink
        self.cad.lcd.cursor_off()
        self.cad.lcd.blink_off()
        
        #Threading: start countdown
        self.t_countdown.daemon = True
        self.t_countdown.start()
        
        #Threading: Play chronometer sound
        self.t_chronometer_sound.daemon = True
        self.t_chronometer_sound.start()

    def register_button_events(self):
        self.listener.register(RED, pifacecad.IODIR_ON, self.button_pressed)
        self.listener.register(GREEN, pifacecad.IODIR_ON, self.button_pressed)
        self.listener.register(YELLOW, pifacecad.IODIR_ON, self.button_pressed)
        self.listener.register(BLUE, pifacecad.IODIR_ON, self.button_pressed)
        self.listener.register(RESET, pifacecad.IODIR_ON, self.button_pressed)
        self.listener.activate()

    def button_pressed(self, event):
        if event.pin_num == RED:
                print('RED')
                self.print_color('RED')
        elif event.pin_num == GREEN:
                print('GREEN')
                self.print_color('GREEN')
        elif event.pin_num == YELLOW:
                print('YELLOW')
                self.print_color('YELLOW')
        elif event.pin_num == BLUE:
                print('BLUE')
                self.print_color('BLUE')
        elif event.pin_num == RESET:
                print('RESET')
                self.print_color('RESET')

    def print_color(self, color):
        self.cad.lcd.set_cursor(0, 1) #second row
        self.cad.lcd.write(color)        
        
    def countdown(self):
        for t in range(self.bomb.bomb_time, -1, -1):
                #self.cad.lcd.clear()
                self.cad.lcd.set_cursor(0, 0)        
                hours, minutes = divmod(t, 3600)
                minutes, seconds = divmod(minutes, 60)        
                sf = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds) 
                print(sf)
                self.cad.lcd.write(sf)
                time.sleep(1)


    def play_chronometer(self):
        #---- Play sound
        os.system('omxplayer chronometer.wav')

    def play_explosion(self):
        #---- Play sound
        os.system('omxplayer explosion.wav')                  

                
if __name__ == "__main__":
    game = BombGame(TIME, CORRECT_SEQUENCE)
    game.start()


