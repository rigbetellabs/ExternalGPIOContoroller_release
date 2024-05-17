from ExternalGPIOController import ExternalGPIOController
import time

# Initialize the GPIO manager
gpio_manager = ExternalGPIOController(port='/dev/ttyUSB0')
gpio_manager.start_daemon()

try:
    while gpio_manager.get_gpio_state(gpio_manager.INPUT_PIN_1) == gpio_manager.PIN_LOW:
        print("Waiting for the GPIO to go low")
        print(gpio_manager.get_gpio_state_all())
        time.sleep(0.1)
    print("GPIO is low now")
    time.sleep(1)
    for i in range(5, 10):
        gpio_manager.set_gpio(i, gpio_manager.PIN_HIGH)
        print("GPIO", i, "set to HIGH")
        time.sleep(1)
    for i in range(5, 10):
        gpio_manager.set_gpio(i, not bool(gpio_manager.get_gpio_state(i)))
        print("GPIO", i, "set to LOW")
        time.sleep(1)
    gpio_manager.stop_daemon()
except KeyboardInterrupt:
    # Stop the daemon gracefully when interrupted
    print("Program interrupted by user.")
except Exception as e:
    # Handle any other exceptions
    print(f"An error occurred: {e}")
finally:
    # Ensure the daemon is stopped in any case
    gpio_manager.stop_daemon()
    print("Daemon stopped and program terminated.")
