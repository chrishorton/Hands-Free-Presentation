import pyautogui
import snowboydecoder
import threading


class DetectorThread (threading.Thread):
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

next_detector = snowboydecoder.HotwordDetector("models/next_slide.pmdl", sensitivity=0.5, audio_gain=1)
previous_detector = snowboydecoder.HotwordDetector("models/previous_slide.pmdl", sensitivity=0.5, audio_gain=1)
next_thread = DetectorThread(next_detector,right_key_press)
previous_thread = DetectorThread(previous_detector, left_key_press)

next_thread.start()
previous_thread.start()

while True:
    pass
