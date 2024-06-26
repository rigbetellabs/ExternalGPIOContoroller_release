# ExternalGPIOController Library Documentation

This documentation provides an example of how to use the `ExternalGPIOController` library to manage GPIO pins.

## 1. Installation
### Installing USB Drivers (For Windows)
Install [CP210x USB to UART Bridge for Serial Communication](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads)

![alt text](Imgs/image.png) 
### Install ExternalGPIOController library
```sh
pip install git+https://github.com/rigbetellabs/ExternalGPIOContoroller_release.git
```

## 2. Usage
Below is an example of how to use the ExternalGPIOController library in your code.
### 1. Importing package and Initialization
#### Importing the library `ExternalGPIOController`
```
from ExternalGPIOController import ExternalGPIOController
```
#### Initialize the GPIO manager object
`Parmeters :` ( `port` = '/dev/ttyUSB0', `baudrate` = 115200, `timeout` = 1) (Default Values)
```python
gpio_manager = ExternalGPIOController(port='COM6', baudrate=115200, timeout=1)
gpio_manager.start_daemon()
```
### How to find Ports
#### For Windows 
Find Port Number on Windows
+ Open Device Manager, and expand the Ports (COM & LPT) list.
+ `COM` Ports will be listed as below
 ![alt text](Imgs/image1.png)

+ Like we can see the `COM` ports is `COM7`

#### For Linux
+ Open terminal and type: ls /dev/*
~~~sh
ls /dev/tty*
~~~ 
![alt text](Imgs/image2.png)

## 3. API Reference

### Input Pins
Input GPIOS are INPUT_PIN_1, INPUT_PIN_2, INPUT_PIN_3, INPUT_PIN_4 and INPUT_PIN_5 Only
For Example We Can read the state Input using `get_gpio_state(pin)` of `INPUT_PIN_1` 
```python
 gpio_manager.get_gpio_state(gpio_manager.INPUT_PIN_1)
``` 
### Output Pins
Outputs Pins for Output are as follows `OUTPUT_PIN_1`,`OUTPUT_PIN_2`,`OUTPUT_PIN_3`,`OUTPUT_PIN_4` and`OUTPUT_PIN_5` only
For Example We Can set the   of `OUTPUT_PIN_1` to `HIGH` 
```python
gpio_manager.set_gpio(gpio_manager.OUTPUT_PIN_1,gpio_manager.PIN_HIGH)) 
``` 
### Pim State
Pin state are indicated by `PIN_HIGH` or `PIN_HIGH` thats for setting Pin to `HIGH or LOW` respectively.
For Example We Can set the   of `OUTPUT_PIN_1` to `HIGH` 
```python
gpio_manager.set_gpio(gpio_manager.OUTPUT_PIN_1,gpio_manager.PIN_HIGH)) 
``` 
### `set_gpio(pin, state)`
+ `Input :` `int` PinNumber , `bool`state
+ `Output :` `int` Returns `0`/ `LOW` or `1` / `HIGH` specifying the state of GPIO  
+  Sets the state of a specified GPIO pin.

### `get_gpio_state(pin)`
+ `Input :` `int` PinNumber
+ `Output :` `int` Returns `0`/ `LOW` or `1` / `HIGH` specifying the state of GPIO  
+  Returns the current state of a specified GPIO pin.
For Example We Can set the   of `OUTPUT_PIN_1` to `HIGH`  using `get_gpio_state(pin)`
```python
gpio_manager.set_gpio(gpio_manager.OUTPUT_PIN_1,gpio_manager.PIN_HIGH)) 
``` 

### `get_gpio_state_all()`
+ `Input :` `None` 
+ `Output :` `int []` Returns array with `0`/ `LOW` or `1` / `HIGH` specifying the state of all GPIO  
+ Returns the current states of all GPIO pins as a dictionary.

```python
# Print the current states of all GPIO pins
print("Current GPIO states:", gpio_manager.get_gpio_state_all())
```

### `start_daemon()`
+ `Input :`  `None` 
+ `Output :` `None` 
+ Starts the GPIO control daemon.
### `stop_daemon()`
+ `Input :`  `None` 
+ `Output :` `None` 
+ Stops the GPIO control daemon.

## Example - 1
### This example reads and toggle the state of OUTPUT_PIN_1
```python
from ExternalGPIOController import ExternalGPIOController
import time

# Initialize the GPIO manager
gpio_manager = ExternalGPIOController() #takes the default port
gpio_manager.start_daemon()

# try:
while True:
    # Toggle the state of OUTPUT_PIN_1
    gpio_manager.set_gpio(gpio_manager.OUTPUT_PIN_1, not bool(gpio_manager.get_gpio_state(gpio_manager.OUTPUT_PIN_1)))
    # Print the current states of all GPIO pins
    print("Current GPIO states:", gpio_manager.get_gpio_state_all())
    # Sleep for a short duration to avoid running the loop too fast
    time.sleep(0.1)
```
## Example - 2
### Read the state at the INPUT_PIN_3 and set the sate of OUTPUT_PIN_3
```python
from ExternalGPIOController import ExternalGPIOController

# Initialize the GPIO manager
gpio_manager = ExternalGPIOController(port='/dev/ttyUSB1') #specifing a port
gpio_manager.start_daemon()

while True:
    
    print(gpio_manager.get_gpio_state_all())
    if gpio_manager.get_gpio_state(gpio_manager.INPUT_PIN_3) == 1:
            gpio_manager.set_gpio(gpio_manager.OUTPUT_PIN_3, gpio_manager.PIN_HIGH)
            print(" 3 is high")
    else:
            gpio_manager.set_gpio(gpio_manager.OUTPUT_PIN_3, gpio_manager.PIN_LOW)
            print(" 3 is low")
```
