import board
import busio
import time
import displayio
import terminalio
from adafruit_display_text import label
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.rgb import RGB
from kmk.modules import Module
import adafruit_displayio_ssd1306 

keyboard = KMKKeyboard()

# keySwitch Matrix

keyboard.col_pins = (board.D0, board.D1, board.D2) 
keyboard.row_pins = (board.D10, board.D9, board.D8) 
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# other components

encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.D6, board.D3, None, False),) 
keyboard.modules.append(encoder_handler)
rgb = RGB(pixel_pin=board.D7, num_pixels=13, val=127) 
keyboard.modules.append(rgb)

# oled display
displayio.release_displays()
i2c = busio.I2C(board.D5, board.D4)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
splash = displayio.Group()
display.show(splash)
status_label = label.Label(terminalio.FONT, text="READY", color=0xFFFFFF, x=10, y=16)
splash.append(status_label)



# keySwitch and encoder maping

keyboard.keymap = [
    [
        KC.F9,                  KC.F10,                 KC.MPLY,
        KC.LCTRL(KC.Z),         KC.LCTRL(KC.C),         KC.LCTRL(KC.V),
        KC.LGUI(KC.LSFT(KC.S)), KC.LCTRL(KC.W),         KC.LGUI(KC.D)
    ]
]
encoder_handler.map = [ ((KC.VOLD, KC.VOLU, None),) ]

# ui state logic
class UIHook(Module):
    def __init__(self):
        self.last_anim_time = time.monotonic()
        self.anim_frame = 0
        self.showing_temp_msg = False
        self.msg_timeout = 0
        self.vol = 10

    def during_bootup(self, keyboard): pass
    def after_matrix_scan(self, keyboard): pass
    def before_hid_send(self, keyboard): pass
    def after_hid_send(self, keyboard): pass

    def before_matrix_scan(self, keyboard):
        curr_time = time.monotonic()
        if not self.showing_temp_msg:
            if curr_time - self.last_anim_time > 0.5:
                frames = ["IDLE .", "IDLE ..", "IDLE ..."]
                status_label.text = frames[self.anim_frame]
                self.anim_frame = (self.anim_frame + 1) % 3
                self.last_anim_time = curr_time
        elif curr_time > self.msg_timeout:
            self.showing_temp_msg = False

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if is_pressed:
            self.showing_temp_msg = True
            self.msg_timeout = time.monotonic() + 1.5
            
            if key == KC.VOLU:
                self.vol = min(20, self.vol + 1)
                bar = "|" * (self.vol // 2)
                status_label.text = f"VOL: [{bar.ljust(10, ' ')}]"
            elif key == KC.VOLD:
                self.vol = max(0, self.vol - 1)
                bar = "|" * (self.vol // 2)
                status_label.text = f"VOL: [{bar.ljust(10, ' ')}]"
            elif key == KC.F9:
                status_label.text = "MIC MUTED"
            elif key == KC.F10:
                status_label.text = "CAM OFF"
            elif key == KC.LCTRL(KC.W):
                status_label.text = "TAB CLOSED"
            else:
                status_label.text = "SENT"
        return key

keyboard.modules.append(UIHook())

if __name__ == '__main__':
    keyboard.go()