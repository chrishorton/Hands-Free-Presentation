import pyautogui
import snowboydecoder
import signal

interrupted = False


def left_key_press():
    pyautogui.press('left')
    print("Heard previous slide - executing left key press")


def right_key_press():
    pyautogui.press('right')
    print("Heard next slide - executing right key press")


def signal_handler(signal_received, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

# Capture and handle CTRL-C
signal.signal(signal.SIGINT, signal_handler)

models = ["models/next_slide.pmdl", "models/previous_slide.pmdl"]
sensitivity_args = [0.5] * len(models)
callbacks = [right_key_press, left_key_press]
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity_args)

print('Now listening for hot words "Next Slide" and "Previous Slide"')

detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback)

detector.terminate()
print("Quitting program...")
