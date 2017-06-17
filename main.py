import pyautogui
from snowboy import snowboydecoder
import signal


def left_key_press():
    pyautogui.press('left')
    print('Heard "previous slide" - executing left key press')


def right_key_press():
    pyautogui.press('right')
    print('Heard "next slide" - executing right key press')


class Detectors(object):
    """
    Wrapper class around detectors to incorporate methods and data
    """

    def __init__(self, detect_models=None, sensitivity=None):
        if detect_models is not None:
            self.models = detect_models
        else:
            self.models = ["models/next_slide.pmdl", "models/previous_slide.pmdl"]

        if sensitivity is not None:
            self.sensitivity_args = sensitivity
        else:
            self.sensitivity_args = [0.5] * len(self.models)

        self.interrupted = False
        self.callbacks = [right_key_press, left_key_press]
        self.detectors = snowboydecoder.HotwordDetector(self.models, sensitivity=self.sensitivity_args)

    def start_detecting(self):
        print('Now listening for hot works "Next Slide" and "Previous Slide"')
        self.interrupted = False
        self.detectors.start(detected_callback=self.callbacks,
                             interrupt_check=lambda: self.interrupted)
        self.detectors.terminate()

    def stop_detecting(self):
        self.interrupted = True


def signal_handler(signal_received, frame):
    detectors.stop_detecting()

if __name__ == '__main__':
    # Capture and handle CTRL-C
    signal.signal(signal.SIGINT, signal_handler)

    detectors = Detectors()
    detectors.start_detecting()

    print("Quitting program...")
