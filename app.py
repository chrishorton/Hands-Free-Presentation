import Tkinter as Tk
import tkFileDialog
import os


class ModelSelect(Tk.Frame):
    """
    Frame for buttons and labels to choose models
    """
    def __init__(self, parent, models, model_edit_callback):
        Tk.Frame.__init__(self, parent)
        self.model_paths = models
        self.model_edit_callback = model_edit_callback
        self.next_model_str = Tk.StringVar()
        self.next_model_str.set("Next Slide model: {}".format(os.path.basename(models[0])))
        self.prev_model_str = Tk.StringVar()
        self.prev_model_str.set("Previous Slide model: {}".format(os.path.basename(models[1])))
        self.init_ui()

    def init_ui(self):
        self.next_model_label = Tk.Label(self, textvariable=self.next_model_str)
        self.next_model_label.grid(row=0, column=0, sticky=Tk.E, padx=5)
        self.prev_model_label = Tk.Label(self, textvariable=self.prev_model_str)
        self.prev_model_label.grid(row=1, column=0, sticky=Tk.E, padx=5)
        self.next_model_button = Tk.Button(self, text="Choose model", command=self.get_next_slide_model)
        self.next_model_button.grid(row=0, column=1, sticky=Tk.W, padx=5)
        self.prev_model_button = Tk.Button(self, text="Choose model", command=self.get_previous_slide_model)
        self.prev_model_button.grid(row=1, column=1, sticky=Tk.W, padx=5)

    def get_next_slide_model(self):
        file_path = tkFileDialog.askopenfilename(
            initialdir="~",
            title="Select Next Slide Model",
            filetypes=(("Snowboy Models", "*.pmdl *.umdl"), ("All Files", "*.*"))
        )
        if file_path:
            file_name = os.path.basename(file_path)
            self.model_paths[0] = file_path
            self.next_model_str.set("Next Slide model: {}".format(file_name))
            self.model_edit_callback()

    def get_previous_slide_model(self):
        file_path = tkFileDialog.askopenfilename(
            initialdir="~",
            title="Select Previous Slide Model",
            filetypes=(("Snowboy Models", "*.pmdl *.umdl"), ("All Files", "*.*"))
        )
        if file_path:
            file_name = os.path.basename(file_path)
            self.model_paths[1] = file_path
            self.prev_model_str.set("Previous Slide model: {}".format(file_name))
            self.model_edit_callback()

    def disable(self):
        self.next_model_button["state"] = Tk.DISABLED
        self.prev_model_button["state"] = Tk.DISABLED

    def enable(self):
        self.next_model_button["state"] = Tk.NORMAL
        self.prev_model_button["state"] = Tk.NORMAL


class DetectApp(Tk.Frame):
    """
    Frame for main app
    """
    def __init__(self, parent, models, sensitivity, recognition, callbacks):
        Tk.Frame.__init__(self, parent)
        self.models = models
        self.sensitivity = sensitivity
        self.recognition = recognition
        self.callbacks = callbacks
        self.changed_vars = False
        self.init_ui()
        self.grid()

    def init_ui(self):
        Tk.Grid.columnconfigure(self, 0, weight=1)
        Tk.Grid.columnconfigure(self, 1, weight=1)
        self.toggle_button = Tk.Button(
            self,
            text="Start Recognition",
            width=25,
            height=2,
            command=self.toggle_detect
        )
        self.toggle_button.grid(row=0, column=0, columnspan=2)
        self.model_select = ModelSelect(self, self.models, self.changed_models)
        self.model_select.grid(row=1, column=0, padx=50)
        self.sensitivity_slider = Tk.Scale(
            self,
            from_=100,
            to=0,
            command=self.changed_sensitivity,
            label="Sensitivity",
            sliderrelief=Tk.GROOVE
        )
        self.sensitivity_slider.set(self.sensitivity * 100)
        self.sensitivity_slider.grid(row=1, column=1, padx=50)

    def changed_models(self):
        self.models = self.model_select.model_paths
        self.changed_vars = True

    def changed_sensitivity(self, num):
        self.sensitivity = float(num) / 100
        self.changed_vars = True

    def toggle_detect(self):
        """
        Toggles detection between on and off
        """
        # If recognition is not currently running
        if not self.recognition.is_running():
            print("Starting recognition...")
            if self.changed_vars:
                self.recognition.change_models(self.models)
                self.recognition.change_sensitivity(self.sensitivity)
                self.changed_vars = False
            self.recognition.start_recog(detected_callback=self.callbacks)
            self.disable_config()
            self.toggle_button["text"] = "Stop Detection"
        else:
            print("Stopping recognition...")
            self.recognition.pause_recog()
            self.enable_config()
            self.toggle_button["text"] = "Start Detection"

    def disable_config(self):
        self.model_select.disable()
        self.sensitivity_slider["state"] = Tk.DISABLED

    def enable_config(self):
        self.model_select.enable()
        self.sensitivity_slider["state"] = Tk.NORMAL
