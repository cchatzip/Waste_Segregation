import time
import RPi.GPIO as GPIO

class InductiveProximitySensor:
    def __init__(self, pin):
        self.pin = pin
        self.initialized = False
    
    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.initialized = True
        print("Finished Initiation")
        print(f"Input Pin: {self.pin}")
    
    def detect_metal(self):
        if not self.initialized:
            raise Exception("Sensor not initialized. Please call initialize() first.")
        
        state = GPIO.input(self.pin)
        if state:
            return
        else:
            return 'Metal Detected'

# Test module
if __name__ == '__main__':
    sensor = InductiveProximitySensor(pin=17)
    sensor.initialize()
    
    try:
        while True:
            sensor.detect_metal()
            time.sleep(0.2)
    except KeyboardInterrupt:
        GPIO.cleanup()  # Ensure GPIO is cleaned up when the script is interrupted 