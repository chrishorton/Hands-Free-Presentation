#!/usr/bin/env python
import Tkinter as tk
import detectors
import signal

root = tk.Tk()
root.title = "Advance your PowerPoint Slides"


def toggle_detect():
    """Toggles detection between on and off"""
    # If recognition is not currently running
    if not recognition.is_running():
        print("Starting recognition...")
        recognition.start_recog()
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
recognition = detectors.Detectors(models, sensitivity)
recognition.start()

# Set up GUI
button = tk.Button(root, text="Start Recognition", width=25, command=toggle_detect)
button.pack()
root.mainloop()
# End recognition and its thread
print("Terminating program")
recognition.terminate()
