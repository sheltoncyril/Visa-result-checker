import time

import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD


class CommonUtils:
    def __init__(self):
        self.lcd = CharLCD("PCF8574", 0x27)
        self.buzzer_pin = 26
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

    def print_delay(self, prnt_str, delay=0.5, *, pre_clear=True, clear_post=False, line=0, char=0):
        if pre_clear:
            self.lcd.clear()
        self.lcd.cursor_pos = (line, char)
        self.lcd.write_string(prnt_str)
        time.sleep(delay)
        if clear_post:
            self.lcd.clear()

    def buzz(self, on=0.5, loop=1, off=None):
        for i in range(loop):
            GPIO.output(self.buzzer_pin, GPIO.HIGH)
            time.sleep(on)
            GPIO.output(self.buzzer_pin, GPIO.LOW)
            if off:
                time.sleep(off)

    def __del__(self):
        self.lcd.close()
        GPIO.cleanup()
