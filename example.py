from ExternalGPIOController import ExternalGPIOController
import time

# Initialize the GPIO manager
gpio_manager = ExternalGPIOController()
gpio_manager.start_daemon()

# try:
while True:
    # Toggle the state of GPIO pin 5
    gpio_manager.set_gpio(gpio_manager.OUTPUT_PIN_1, not bool(gpio_manager.get_gpio_state(gpio_manager.OUTPUT_PIN_1)))
    # Print the current states of all GPIO pins
    print("Current GPIO states:", gpio_manager.get_gpio_state_all())
    # Sleep for a short duration to avoid running the loop too fast
    time.sleep(0.1)
