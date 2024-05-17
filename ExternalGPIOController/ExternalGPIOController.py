#!/usr/bin/env python3

import threading
import subprocess
import re
import time
import serial
import signal
import sys

class ExternalGPIOController:
    PIN_HIGH = True
    PIN_LOW = False
    
    INPUT_PIN_1 = 0
    INPUT_PIN_2 = 1
    INPUT_PIN_3 = 2
    INPUT_PIN_4 = 3
    INPUT_PIN_5 = 4

    OUTPUT_PIN_1 = 5
    OUTPUT_PIN_2 = 6
    OUTPUT_PIN_3 = 7
    OUTPUT_PIN_4 = 8
    OUTPUT_PIN_5 = 9

    def __init__(self,port='/dev/ttyUSB0',baudrate=115200, timeout=1,sig=signal.SIGINT):
        NUM_OF_GPIO_PINS = 10
        self.port = port
        self.baudrate = baudrate
        self.timeout =timeout
        self.serial_instance = self.connect_to_serial(self.port, self.baudrate, self.timeout)
        self.read_thread = None
        self.read_lock = False
        self.stop_event = threading.Event()
        signal.signal(sig, self.Interrupt_handler)
        self.gpio_states = [0] * NUM_OF_GPIO_PINS
    
    def Interrupt_handler(self,signal,frame):
        self.stop_daemon()
        print("User pressed Ctrl+C! Daemon stopped")

    def connect_to_serial(self, port, baudrate=115200, timeout=1):
        try:
            serial_instance = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            serial_instance.reset_input_buffer()
            serial_instance.reset_output_buffer()
            print("Connected to", port)
            return serial_instance
        except serial.SerialException as e:
            print("Error connecting to serial port:", e)
            return None
    
    def read_from_serial(self):
        while not self.stop_event.is_set():
            if self.serial_instance:
                if self.read_lock:
                    continue
                try:
                    line = self.serial_instance.readline().decode('utf-8').strip()
                    self.serial_instance.reset_input_buffer()
                    
                    if line.startswith("GPIO states: [") and line.endswith("]") and len(line)==43:
                        gpio_states_str = line.replace("GPIO states: [", "").replace("]", "")
                        try:
                            gpio_states = list(map(int, gpio_states_str.split(", ")))
                            self.gpio_states = gpio_states
                        except ValueError as ve:
                            print(f"ValueError: {ve} - Received data: {gpio_states_str}")
                except UnicodeDecodeError:
                    print("UnicodeDecodeError: Unable to decode some bytes in the received data.")
                except serial.SerialException as serial_error:
                    print("Serial Error:", serial_error)
                    self.serial_instance = None
            else:
                self.reconnect_serial()

        print("Exiting read thread")


    def set_gpio(self, output_pin_number, value):
        if self.serial_instance:
            self.read_lock = True
            command = f"{output_pin_number},{'HIGH' if value else 'LOW'}"
            try:
                self.serial_instance.write(bytes(command.encode('utf-8')))
                self.serial_instance.flush()
            except serial.SerialException as serial_error:
                print("Serial Error:", serial_error)
                self.serial_instance = None
            self.read_lock = False
        else:
            self.reconnect_serial()

    def reconnect_serial(self):
        # Reconnect if serial disconnected
        while not self.serial_instance or not self.serial_instance.is_open:
            print("Reconnecting...")
            self.serial_instance = self.connect_to_serial(self.port, self.baudrate, self.timeout)
            if self.serial_instance:
                break
            time.sleep(1)  # Wait before trying to reconnect again

    def start_daemon(self):
        self.read_thread = threading.Thread(target=self.read_from_serial)
        self.read_thread.daemon = True
        self.read_thread.start()
        print("Daemon started")

    def stop_daemon(self):
        self.stop_event.set()
        if self.read_thread:
            self.read_thread.join()
        self.read_thread = None
        print("Daemon stopped")
    
    def get_gpio_state(self, input_pin_number):
        return self.gpio_states[input_pin_number]
        
    def get_gpio_state_all(self):
        return self.gpio_states
    def Interrupt_handler(self,signal, frame):
        print("You pressed Ctrl+C - or killed me with -2")
        self.stop_daemon()
        sys.exit(0)