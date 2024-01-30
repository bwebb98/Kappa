import tkinter as tk
from tkinter import *
from customtkinter import CTkButton
import matplotlib as mpl
from reportlab.platypus import Paragraph
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_pdf import PdfPages
import latex2sympy2
import numpy as np
from sympy import symbols, preview, Symbol
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
plt.rcParams['toolbar'] = 'None'
from elements import *

root = tk.Tk()
setRoot(root)
root.title("Kappa Editor")

# Set the height and width of the app to the size of the screen
winWidth = root.winfo_screenwidth()
winHeight = root.winfo_screenheight()
root.geometry("%dx%d" % (winWidth-100, winHeight-100, ))

#create canvas for the display of the text entered
disp_frame = Frame(root, bg="blue")
disp_frame.grid(rowspan=2, column = 1, columnspan = 2, padx=30, sticky="news")
root.grid_rowconfigure(1, weight=1)  # This gives extra vertical space to the second row (index 1)
root.grid_columnconfigure(1, weight=0)  # This gives extra horizontal space to the second column (index 1)
root.grid_columnconfigure(2, weight=1)
sidebar2_canvas = Canvas(disp_frame, highlightbackground="grey", highlightthickness=1, bg="white")
sidebar2_canvas.grid(row = 0, column=0, sticky="nsew")
disp_frame.grid_rowconfigure(0, weight=1)
disp_frame.grid_columnconfigure(0, weight=1)
disp_frame.grid_columnconfigure(1, weight=0)

setSidebar2_canvas(sidebar2_canvas)

# Top bar menu
menu = Menu(root)
root.config(menu=menu)

# Top bar menu
main_menu = Menu(root)
root.config(menu=main_menu)

# File menu
file_menu = Menu(main_menu, tearoff=0)  # tearoff=0 removes the dashed line at the top of the menu
file_menu.add_command(label="Open", command=open_file)  # Replace with your function
file_menu.add_command(label="Save Questions", command=save_fileList)  # Replace with your function
file_menu.add_command(label="Save as PDF", command=save_canvas)  # Replace with your function
file_menu.add_command(label="Exit", command=root.quit)
main_menu.add_cascade(label="File", menu=file_menu)

# Edit menu
edit_menu = Menu(main_menu, tearoff=0)

#Removed since not really needed
#edit_menu.add_command(label="Undo", command=None)  # Replace with undo
#edit_menu.add_command(label="Redo", command=None)  # Replace with redo

edit_menu.add_command(label="Header", command=edit_header) # Replace with header editer
main_menu.add_cascade(label="Edit", menu=edit_menu)

# Initialization of left-side sidebar
sidebar_frame = tk.Frame(root, bg="grey")
sidebar_frame.grid(row=0, column=0, sticky="nsw")
setSidebar_frame(sidebar_frame)

#handles anything that needs to be cleaned up when we close the window
root.protocol("WM_DELETE_WINDOW", closing)


file_list = DragDropListbox(sidebar_frame, exportselection=False)
file_list.grid(row=1, column=0, columnspan=2, sticky="nsew")

setFile_list(file_list)

# Button to Add Title to the canvas (canvas can't get text if entry is set in the grid early)
inputTitle = Entry(sidebar_frame)
Display = CTkButton(sidebar_frame, text="Insert Title", command=lambda: Get_Title(inputTitle.get()))
Display.grid(row=4, column=1, pady=10)
inputTitle.grid(row=4, column=0, pady=5)

add_file_button = CTkButton(sidebar_frame, text="Add File", command=open_file)
add_file_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

add_text_button = CTkButton(sidebar_frame, text="+ New Question", command=add_text)  # Replace '' with the desired command
add_text_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

deleteQuestionButt = CTkButton(sidebar_frame, text="Delete", command=lambda :deleteQues())
deleteQuestionButt.grid(row=2, column=0, padx=5, pady=5, sticky="w")

editQuestionButt = CTkButton(sidebar_frame, text="Edit Question", command=edit_Question)
editQuestionButt.grid(row=2, column=1, padx=5, pady=5, sticky="w")

#setup the scrollbar
scroll = tk.Scrollbar(root, orient=VERTICAL, command=sidebar2_canvas.yview)
scroll.grid(row=0, rowspan=2, column=3, sticky='ns')
sidebar2_canvas.configure(yscrollcommand=scroll.set)
sidebar2_canvas.bind('<Configure>', lambda e: sidebar2_canvas.configure(scroll = sidebar2_canvas.bbox("all")))
second_frame = Frame(sidebar2_canvas)
sidebar2_canvas.create_window((0,0), window=second_frame, anchor="nw")

# Configure the rows and columns for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
sidebar_frame.grid_rowconfigure(1, weight=1)
sidebar_frame.grid_columnconfigure(0, weight=1)
sidebar_frame.grid_columnconfigure(1, weight=1)

root.mainloop()
