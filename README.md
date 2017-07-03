# Hands-Free Presentation
A useful application that allows you to deliver presentations solely with your voice. Move between slides using hotwords rather than your laptop's arrow keys or a clicker.

##  Installation
* [Python 2.7](https://www.python.org/downloads/) - Python 3 is currently not supported
* [Snowboy](https://snowboy.kitt.ai/) - hotword detection 
* [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) - sending soft keypresses to manipulate presentations 

Unfortunately, Snowboy currently is not supported on Windows, therefore making this application unavailable on Windows as of right now. However, if you are running OSX or an Ubuntu-based system, this application will work just fine. It may be possible to run on Windows by following the Ubuntu installation instructions using Bash on Windows, but that is currently untested.


Both Snowboy and PyAutoGUI require their own dependencies. Instructions for installation are listed below, or you can use the following links. 

Snowboy's dependencies are documented [here](https://github.com/Kitt-AI/snowboy/blob/master/README.md#dependencies), and PyAutoGUI's dependencies are found [here](https://pyautogui.readthedocs.io/en/latest/install.html#installation). However, since this application only uses Python 2, make sure to replace `pip3` with `pip` and `python3` with `python` in PyAutoGUI's installation instructions. The commands for installing dependencies are also written below.

**OSX Installation**

Open up a terminal and run:
```bash
brew install swig portaudio sox
pip install pyaudio
pip install pyobjc-core
pip install pyobjc
pip install pyautogui
```
Depending on your system, you may have to run `sudo pip install` rather than `pip install`.

If you do not have Homebrew installed, please download it [here](http://brew.sh/). If you don't have `pip`, you can install it [here](https://pip.pypa.io/en/stable/installing/).

**Ubuntu Installation**

Open up a terminal and run:
```bash
sudo apt-get install swig3.0 sox portaudio19-dev
pip install pyaudio
sudo apt-get install libatlas-base-dev
sudo apt-get install python-dev
sudo apt-get install python-xlib python-tk
pip install pyautogui
```

Again, depending on how your system is set up, you may have to run `sudo pip install` rather than `pip install`.

If you run into issues installing these dependencies, please look at the documentations for Snowboy and PyAutoGUI linked above. If you still cannot install them, post an issue on this Github.

## Usage
To download this application, use the **Clone or Download** button at the top-right corner of this page. You can either download it as a ZIP and then extract it, or you can clone the repository if your system has git installed.

Since we do not have universal Snowboy models available yet, you need personal Snowboy models for detecting the hotwords **Next Slide** and **Previous Slide** to use this application. The application ships with two example models, but they are personal models that are not likely to work well with your voice. To make your own personal models, first create an account on [Snowboy](https://snowboy.kitt.ai/). Then, record three voice samples for the [Next Slide Model](https://snowboy.kitt.ai/hotword/7485) and [Previous Slide Model](https://snowboy.kitt.ai/hotword/7486). For best results, record in a fairly silent environment with the same microphone each time, and make sure to record yourself saying the hotwords as similarly as possible to how you would say them in a presentation. Submitting your own voice samples also helps us progress towards obtaining universal Snowboy models, and makes our hotword detection better.

After recording your three voice samples for either hotword, download the models for both hotwords. They should have a `.pmdl` extension. 

To run the application, simply run the bash script `run.sh`. The first time this is run, it will automatically handle initial setup and configuration before running the application. Once the application launches, locate and select your two models through the user interface. At this point, you're all set! Before your presentations, start detection with the **Start detection** button, and stop detection in the same manner. You can also configure the sensitivity through the user interface. If the application is struggling to recognize the hotwords, raise the sensitivity. If it is detecting hotwords when you did not say any, lower the sensitivity.

If you find this application useful, please show it to others and encourage them to try it out. It will greatly support our development.
