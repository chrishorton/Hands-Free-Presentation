#!/usr/bin/env python
import Tkinter as tk
from app import DetectApp
import detectors
import signal
import pyautogui
import json



def left_key_press():
    pyautogui.press('left')
    print('Heard "previous slide" - executing left key press')


def right_key_press():
    pyautogui.press('right')
    print('Heard "next slide" - executing right key press')


def signal_handler(signal_received, frame):
    print("Signal handler - SIGINT")
    root.destroy()

signal.signal(signal.SIGINT, signal_handler)


# Initialize thread to run detectors
with open("config.json", "r") as json_data:
    detection_data = json.load(json_data)

models = detection_data["models"]
sensitivity = detection_data["sensitivity"]
callbacks = [right_key_press, left_key_press]
recognition = detectors.Detectors(models, sensitivity=sensitivity)
recognition.start()

# Set up GUI
root = tk.Tk()
root.resizable(0, 0)
root.title = "Hands-Free Presentation"
app = DetectApp(root, models, sensitivity, recognition, callbacks)
root.mainloop()  # Blocks until GUI is closed

# End recognition and its thread
print("Terminating program")
recognition.terminate()

# Save configurations to config.json
config_data = {
    "models": app.models,
    "sensitivity": app.sensitivity
}
with open("config.json", "w") as json_file:
    json.dump(config_data, json_file)
