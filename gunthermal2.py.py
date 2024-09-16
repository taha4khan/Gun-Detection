import cv2
import numpy as np
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

# Create an event to signal the camera loop to stop
stop_event = threading.Event()

# Function to start buzzing three times and then close the application
def start_buzzing():
    def buzz():
        time.sleep(3)
        for _ in range(3):
            buzzer_on()
            time.sleep(1)
            buzzer_off()
            time.sleep(1)
        on_closing()  # Close the application after buzzing

    threading.Thread(target=buzz).start()

# Function to clean up GPIO and stop the camera loop on exit
def on_closing():
    stop_event.set()  # Signal the camera loop to stop
    GPIO.cleanup()
    root.destroy()
    cv2.destroyAllWindows()
    exit(0)  # Ensure the program is fully terminated

# Function to apply the thermal filter to a frame
def apply_thermal_filter(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply a color map to the grayscale image to create a thermal effect
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    
    return thermal

# Function to start the video capture and thermal filter application
def camera_loop():
    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    while not stop_event.is_set():
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Apply the thermal filter
        thermal_frame = apply_thermal_filter(frame)
        
        # Display the resulting frame
        cv2.imshow('Thermal Camera View', thermal_frame)
        
        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

# Create the main window
root = tk.Tk()
root.title("Buzzer Control")

# Create and place buttons
start_buzzer_button = tk.Button(root, text="Run Detection", command=start_buzzing)
start_buzzer_button.pack(pady=10)

# Set the closing event to clean up GPIO
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the camera loop in a separate thread
camera_thread = threading.Thread(target=camera_loop)
camera_thread.start()

# Start the GUI event loop
root.mainloop()
