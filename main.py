from os import stat
from tkinter import StringVar, font, image_names
from typing import Collection
import moviepy.editor
import tkinter as tk
from tkinter import Button, Entry, Label, StringVar, ttk
from tkinter.filedialog import *
from PIL import Image
from pytube import YouTube 

def open_file():
    video = askopenfilename()
    video = moviepy.editor.VideoFileClip(video)
    audio = video.audio
    audio.write_audiofile("sample.mp3")
    status.config(text="Status: Converted!", fg="green")


window = tk.Tk()
window.geometry("500x300")
window.title("Simple Converter")
window.resizable(False, False)


def jpg_to_png():
    filename=askopenfilename()
    if filename.endswith('.jpg'):
        Image.open(filename).save("Sample.png")



def png_to_ico():
    filename=askopenfilename()
    if filename.endswith('.png'):
        Image.open(filename).save("Sample.ico")
        Image.open(filename).save("Sample.ico")

    


label = tk.Label(window, text="Convert mp4 to mp3", font=("Raleway", 13))
label.place(x=25, y=10)

button1 = tk.Button(window, text="Convert", command=open_file, bg="#dcdadd", height=1, width=15)
button1.place(x=28, y=75)

label2 = tk.Label(window, text="Image converter:",font=("Raleway", 13))
label2.place(x=25,y=140)

button3 = Button(window, text="Png to Ico", command=png_to_ico, bg="#dcdadd", height=1, width=15)
button3.place(x=25, y=180)


button4 = Button(window, text="Jpg to Png", command=jpg_to_png, bg="#dcdadd", height=1, width=15)
button4.place(x=25, y=220)


credits = tk.Label(window, text="Author: DarkSnake", font=("Raleway",10))
credits.place(x=375, y=275)
version = tk.Label(window, text="Version 1.0", font=("Raleway",10))
version.place(x=10, y=275)


#ytb downloader
Folder = ""

def open_folder():
    global Folder
    Folder = askdirectory()
    if(len(Folder) > 1):
        locationError.config(text=Folder,fg="green")

    else:
        locationError.config(text="Select a path!")

def downloadVideo():
    choices = ytfeatures.get()
    url = entryBox.get()

    if(len(url)>1):
        error.config(text="")
        yt = YouTube(url)

        if(choices == features[0]):
            select = yt.streams.filter(progressive=True).last()

        elif(choices == features[1]):
            select = yt.streams.filter(only_audio=True).first()

        else:
            error.config(text="Paste a link")

    select.download(Folder)
    error.config(text="Download Completed!", fg="green")


laberl1 = tk.Label(window, text="Ytb Mp3/Mp4 Downloader", font=("Raleway", 13))
laberl1.place(x=290, y= 10)

entryBoxvar = StringVar()
entryBox = tk.Entry(window, width=30, textvariable=entryBoxvar)
entryBox.place(x=290, y=40)


error = Label(window,text="Status: not downloaded",fg="red",font=("jost",10))
error.place(x=310, y=60)

status = tk.Label(window, text="Status: not converted", fg="red", font=("Raleway", 10))
status.place(x=25, y=40)

savethevideo = tk.Label(window, text="Choose path for download:", font=("jost",10))
savethevideo.place(x=308, y= 85)


saveEntry = tk.Button(window, text="Save Path", bg="#dcdadd", command=open_folder, width=25)
saveEntry.place(x=290, y= 110)


locationError = tk.Label(window,text="",fg="red",font=("jost",10))
locationError.place(x=290, y=140)


feature = tk.Label(window,text="Select feature",font=("jost",10))
feature.place(x=340, y=165)


features = ["Mp4 Video", "Mp3 Audio"]
ytfeatures = ttk.Combobox(window, values=features)
ytfeatures.place(x=313, y=190)


downloadButton = tk.Button(window, text="Download", width=25, bg="#dcdadd", command=downloadVideo)
downloadButton.place(x=290, y=220)



if __name__ == "__main__":
    window.mainloop()
