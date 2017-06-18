import pyautogui
from snowboy import snowboydecoder
import threading
import Queue


def left_key_press():
    pyautogui.press('left')
    print('Heard "previous slide" - executing left key press')


def right_key_press():
    pyautogui.press('right')
    print('Heard "next slide" - executing right key press')


class Detectors(threading.Thread):
    """
    Wrapper class around detectors to run them in a separate thread
    and provide methods to pause, resume, and modify detection
    """

    def __init__(self, models, sensitivity=0.5):
        threading.Thread.__init__(self)
        self.models = models
        self.sensitivity = [sensitivity] * len(self.models)
        self.interrupted = True
        self.commands = Queue.Queue()
        self.callbacks = [right_key_press, left_key_press]
        self.vars_are_changed = True
        self.detectors = None  # Initialize when thread is run

    def initialize_detectors(self):
        """
        Returns initialized Snowboy HotwordDetector objects
        """
        return snowboydecoder.HotwordDetector(self.models, sensitivity=self.sensitivity)

    def run(self):
        """
        Runs in separate thread - waits on command to either run detectors or terminate thread from commands queue
        """
        try:
            while True:
                command = self.commands.get(True)
                if command == "Start":
                    self.interrupted = False
                    if self.vars_are_changed:
                        self.detectors = self.initialize_detectors()
                        self.vars_are_changed = False
                    print('Now listening for hot words "Next Slide" and "Previous Slide"')
                    # Start detectors - blocks until interrupted by self.interrupted variable
                    self.detectors.start(detected_callback=self.callbacks,
                                         interrupt_check=lambda: self.interrupted)

                    print('Command recognition stopped.')
                elif command == "Terminate":
                    # Program ending - terminate thread
                    break
        finally:
            self.detectors.terminate()

    def start_recog(self):
        """
        Starts recognition in thread
        """
        self.commands.put("Start")

    def stop_recog(self):
        """
        Stops recognition in thread
        """
        self.interrupted = True

    def terminate(self):
        """
        Terminates recognition thread - called when program terminates
        """
        self.stop_recog()
        self.commands.put("Terminate")

    def is_running(self):
        return not self.interrupted

    def change_models(self, models):
        if self.is_running():
            print("Cannot modify detectors while running")
            return
        self.models = models
        self.callbacks = right_key_press
        self.sensitivity = 0.5
        self.vars_are_changed = True
        print("Changed models")

    def change_sensitivity(self, sensitivity):
        if self.is_running():
            print("Cannot modify detectors while running")
            return
        if sensitivity is not list:
            sensitivity = [sensitivity] * len(self.models)
        self.sensitivity = sensitivity
        self.vars_are_changed = True
        print("Changed sensitivity")
