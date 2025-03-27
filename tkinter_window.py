import sqlite3 as SQL
import tkinter
from tkinter import messagebox


def main_window():
    window = tkinter.Tk()
    window.title('Welkom')

    frame = tkinter.Frame(window)
    frame.pack(padx=30, pady=30)

    first_label = tkinter.Label(frame, text='Dit is een label')
    first_label.grid(row=0, column=0)
    first_entry_box = tkinter.Entry(frame)
    first_entry_box.grid(row=1, column=0)

    second_label = tkinter.Label(frame, text='Nog een label')
    second_label.grid(row=0, column=1)
    second_entry_box = tkinter.Entry(frame)
    second_entry_box.grid(row=1, column=1)

    label_frame = tkinter.LabelFrame(frame, text='Dit is een LabelFrame')
    label_frame.grid(row=2, column=0, columnspan=2, pady=15, sticky='ew')

    nested_label = tkinter.Label(label_frame, text='Dit is de eerste Label in LabelFrame')
    nested_label.grid(row=0, column=0, sticky='w')
    nested_entry = tkinter.Entry(label_frame)
    nested_entry.grid(row=1, column=0, sticky='w')

    second_nested_label = tkinter.Label(label_frame, text='Dit is de tweede label')
    second_nested_label.grid(row=0, column=1, sticky='w')
    second_nested_entry = tkinter.Entry(label_frame)
    second_nested_entry.grid(row=1, column=1, sticky='w')

    button_label_frame = tkinter.LabelFrame(frame, text='Dit zijn buttons')
    button_label_frame.grid(row=3, column=0, columnspan=2)

    first_button = tkinter.Button(button_label_frame, text='1st Button')
    second_button = tkinter.Button(button_label_frame, text='2nd Button')
    first_button.grid(row=0, column=0, padx=15, pady=15)
    second_button.grid(row=0, column=1, padx=15, pady=15)

    window.mainloop()

main_window()