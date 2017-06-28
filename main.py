#!/usr/bin/env python
import Tkinter as tk
import detectors
import signal
import pyautogui


def left_key_press():
    pyautogui.press('left')
    print('Heard "previous slide" - executing left key press')


def right_key_press():
    pyautogui.press('right')
    print('Heard "next slide" - executing right key press')


def toggle_detect():
    """Toggles detection between on and off"""
    # If recognition is not currently running
    if not recognition.is_running():
        print("Starting recognition...")
        recognition.start_recog(detected_callback=callbacks)
        button["text"] = "Stop Detection"
    else:
        print("Stopping recognition...")
        recognition.stop_recog()
        button["text"] = "Start Detection"


def signal_handler(signal_received, frame):
    print("Signal handler - SIGINT")
    root.destroy()

signal.signal(signal.SIGINT, signal_handler)

# Initialize thread to run detectors
models = ["models/next_slide.pmdl", "models/previous_slide.pmdl"]
sensitivity = 0.5
callbacks = [right_key_press, left_key_press]
recognition = detectors.Detectors(models, sensitivity=sensitivity)
recognition.start()

# Set up GUI
root = tk.Tk()
root.title = "Advance your PowerPoint Slides"
button = tk.Button(root, text="Start Recognition", width=25, command=toggle_detect)
button.pack()
root.mainloop()
# End recognition and its thread
print("Terminating program")
recognition.terminate()
