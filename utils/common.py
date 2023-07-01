import time

from RPLCD.i2c import CharLCD


class CommonUtils:
    def __init__(self):
        self.lcd = CharLCD("PCF8574", 0x27)


def print_delay(self, prnt_str, *, pre_clear=True, clear_post=False, delay=1, line=0, char=0):
    if pre_clear:
        self.lcd.clear()
    self.lcd.cursor_pos = (line, char)
    self.lcd.write_string(prnt_str)
    time.sleep(delay)
    if clear_post:
        self.lcd.clear()


def __del__(self):
    self.lcd.close()
