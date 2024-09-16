import tkinter as tk
import RPi.GPIO as GPIO
import time
import threading

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO pin 21 as output
buzz_pin = 21
GPIO.setup(buzz_pin, GPIO.OUT)

# Function to turn the buzzer on
def buzzer_on():
    GPIO.output(buzz_pin, GPIO.HIGH)

# Function to turn the buzzer off
def buzzer_off():
    GPIO.output(buzz_pin, GPIO.LOW)

# Function to start buzzing three times
def start_buzzing():
    def buzz():
        for _ in range(3):
            buzzer_on()
            time.sleep(1)
            buzzer_off()
            time.sleep(1)
    
    threading.Thread(target=buzz).start()

# Function to stop buzzing (not used in this case but kept for completeness)
def stop_buzzing():
    buzzer_off()

# Function to clean up GPIO on exit
def on_closing():
    GPIO.cleanup()
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Buzzer Control")

# Create and place buttons
start_button = tk.Button(root, text="Run Code", command=start_buzzing)
start_button.pack(pady=10)

# Set the closing event to clean up GPIO
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI event loop
root.mainloop()
