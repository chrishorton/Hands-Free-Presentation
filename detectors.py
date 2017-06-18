from snowboy import snowboydecoder
import threading
import Queue


class Detectors(threading.Thread):
    """
    Wrapper class around detectors to run them in a separate thread
    and provide methods to pause, resume, and modify detection
    """

    def __init__(self, models, **kwargs):
        """
        Initialize Detectors object. **kwargs is for any __init__ keyword arguments to be passed into HotWordDetector
        __init__() function.
        """
        threading.Thread.__init__(self)
        self.models = models
        self.init_args = kwargs
        self.interrupted = True
        self.commands = Queue.Queue()
        self.vars_are_changed = True
        self.detectors = None  # Initialize when thread is run
        self.run_args = None  # Initialize when detectors start

    def initialize_detectors(self):
        """
        Returns initialized Snowboy HotwordDetector objects
        """
        self.detectors = snowboydecoder.HotwordDetector(self.models, **self.init_args)

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
                        self.initialize_detectors()
                        self.vars_are_changed = False
                    print('Now listening for hot words "Next Slide" and "Previous Slide"')
                    # Start detectors - blocks until interrupted by self.interrupted variable
                    self.detectors.start(interrupt_check=lambda: self.interrupted, **self.run_args)

                    print('Command recognition stopped.')
                elif command == "Terminate":
                    # Program ending - terminate thread
                    break
        finally:
            self.detectors.terminate()

    def start_recog(self, callbacks, sleep_time=0.03):
        """
        Starts recognition in thread. Accepts optional to pass into the HotWordDetector.start() function, but
        does not accept interrupt_callback
        """
        self.run_args = {"detected_callback": callbacks, "sleep_time": 0.03}
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
        if models is not list:
            models = [models]
        self.models = models
        self.vars_are_changed = True
        print("Changed models")

    def change_sensitivity(self, sensitivity):
        if self.is_running():
            print("Cannot modify detectors while running")
            return
        if sensitivity is not list:
            sensitivity = [sensitivity] * len(self.models)
        self.init_args['sensitivity'] = sensitivity
        self.vars_are_changed = True
        print("Changed sensitivity")
