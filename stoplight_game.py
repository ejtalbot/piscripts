import random
import RPi.GPIO as GPIO
import time

class Light:
    def __init__(self, pin: int, color: str):
        self.pin = pin
        self.color = color
        GPIO.setup(self.pin, GPIO.OUT)
    
    def __repr__(self):
        return repr(f"{self.color} light")

    def __eq__(self, other):
        return self.pin == other

    def __hash__(self):
        return self.pin

    def turn_on(self):
        print(f"Turning on {self}")
        GPIO.output(self.pin, 1)

    def turn_off(self):
        print(f"Turning off {self}")
        GPIO.output(self.pin, 0)

    def blink(self, duration):
        self.turn_on()
        time.sleep(duration)
        self.turn_off()
        time.sleep(duration)
    
    def check_status(self):
        try:
            if GPIO.input(self.pin) ==1:
                print(f"{self} is on")
            else:
                print(f"{self} is off")
        except Exception as e:
            print(f"Unable to determine status of {self}")

class Board:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.lights = dict()
        self.setup_lights()

    def create_light(self, pin, color):
        self.lights[pin] = Light(pin, color)

    def setup_lights(self):
        pin_color_mapping = {
            7: "red",
            11: "yellow",
            13: "green"
        }
        for pin, color in pin_color_mapping.items():
            self.create_light(pin, color)


def main():
    board = Board()
    for i in range (10):
        for pin, light in board.lights.items():
            light.blink(.1*random.randint(1, 9))
    GPIO.cleanup()

if __name__=="__main__":
    main()