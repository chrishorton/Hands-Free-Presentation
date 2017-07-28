#!/usr/bin/env python
import Tkinter as Tk
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
resource = detection_data["resource"]
callbacks = [right_key_press, left_key_press]
recognition = detectors.ThreadedDetector(models, sensitivity=sensitivity, resource=resource)
recognition.start()

# Set up GUI
root = Tk.Tk()
root.resizable(0, 0)  # Prevents resizing of GUI
root.title("Hands-Free Presentation")
app = DetectApp(root, models, sensitivity, recognition, callbacks)
root.mainloop()  # Blocks until GUI is terminated

# End recognition and its thread
print("Closing application...")
recognition.terminate()

# Save configurations to config.json
detection_data["models"] = app.models
detection_data["sensitivity"] = app.sensitivity
with open("config.json", "w") as json_file:
    json.dump(detection_data, json_file)
