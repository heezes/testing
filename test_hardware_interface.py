import time
try:
    from gpiozero import LED, Button
except:
    pass

class hardware():
    def __init__(self, pins):
        self.pins = []
        # self.device_reset()
        for i in range(0, len(pins)):
            try:
                self.pins.append(LED(pins[i]))
                self.pins[i].off()
            except:
                print(i)
    def device_reset(self):
        try:
            reset_pin = LED(5)
            reset_pin.on()
            time.sleep(1)
            reset_pin.off()
        except:
            pass
    def enable_gpio(self, pin_idx):
        try:
            self.pins[pin_idx].on()
        except:
            pass
    def disable_gpio(self, pin_idx):
        try:
            self.pins[pin_idx].off()
        except:
            pass

    def toggle_gpio(self, pin_idx):
        self.pins[pin_idx].toggle()

