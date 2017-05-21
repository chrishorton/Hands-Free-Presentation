import pyautogui
from snowboy import snowboydecoder
import threading
import time


class DetectorThread (threading.Thread):
    """
    Thread class for the separate detectors to detect simultaneously
    """
    def __init__(self, detector, callback):
        threading.Thread.__init__(self)
        self.detector = detector
        self.callback = callback
        self.daemon = True

    def run(self):
        self.detector.start(self.callback)


def left_key_press():
    pyautogui.press('left')


def right_key_press():
    pyautogui.press('right')

next_slide_detector = snowboydecoder.HotwordDetector("models/next_slide.pmdl", sensitivity=0.5, audio_gain=1)
previous_slide_detector = snowboydecoder.HotwordDetector("models/previous_slide.pmdl", sensitivity=0.5, audio_gain=1)

next_slide_thread = DetectorThread(next_slide_detector, right_key_press)
previous_slide_thread = DetectorThread(previous_slide_detector, left_key_press)

next_slide_thread.start()
previous_slide_thread.start()

# Hack to keep main thread running, as since the child threads are daemon threads, main thread can terminate them
while True:
    # Hack to reduce CPU usage significantly
    time.sleep(100)
