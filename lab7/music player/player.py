from tkinter import filedialog
import pygame
import os
from tkinter import *

pygame.init()

root = Tk()
root.title('Music Player')
root.geometry("500x320")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False

def load_music():
    global songs
    root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)

    songlist.delete(0, END)
    for song in songs:
        songlist.insert(END, song)

def play_music():
    global current_song, paused

    if not paused:
        current_song = songlist.get(ACTIVE)
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused

    try:
        next_index = songs.index(current_song) + 1
        if next_index >= len(songs):
            next_index = 0
        current_song = songs[next_index]
        songlist.selection_clear(0, END)
        songlist.selection_set(next_index)
        songlist.activate(next_index)
        play_music()
    except IndexError:
        pass

def prev_music():
    global current_song, paused

    try:
        prev_index = songs.index(current_song) - 1
        if prev_index < 0:
            prev_index = len(songs) - 1
        current_song = songs[prev_index]
        songlist.selection_clear(0, END)
        songlist.selection_set(prev_index)
        songlist.activate(prev_index)
        play_music()
    except IndexError:
        pass

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organise', menu=organise_menu)

songlist = Listbox(root, bg="black", fg="white", width=100, height=15)
songlist.pack()

play_btn_image = PhotoImage(file='play.png')
pause_btn_image = PhotoImage(file='pause.png')
next_btn_image = PhotoImage(file='next.png')
prev_btn_image = PhotoImage(file='previous.png')

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

root.mainloop()
