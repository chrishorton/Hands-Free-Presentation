import pyautogui
import snowboydecoder


def left_key_press():
    pyautogui.press('left')


def right_key_press():
    pyautogui.press('right')


def main():
    next_detector = snowboydecoder.HotwordDetector("models/next_slide.pmdl", sensitivity=0.5, audio_gain=1)
    previous_detector = snowboydecoder.HotwordDetector("models/previous_slide.pmdl", sensitivity=0.5, audio_gain=1)
    next_detector.start(right_key_press)
    previous_detector.start(left_key_press)

if __name__=='__main__':
    main()