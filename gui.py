import Tkinter as tk
import main

root = tk.Tk()
root.title = "Advance your PowerPoint Slides"

def start_recog():
    '''Starts main recognition thread with options specified from drag gui elements'''
    print("Starting recognition...")
    main.start_recognition()




def start_button(button):
    def start_listener():
        button.pack()


button = tk.Button(root, text="Start", width=25,command=start_recog)
start_button(button)
button.pack()
root.mainloop()