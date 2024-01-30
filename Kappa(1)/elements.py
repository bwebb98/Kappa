import tkinter as tk
from tkinter import *
import numpy as np
import os
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from customtkinter import CTkButton
import matplotlib as mpl
mpl.use("TkAgg")
from PIL import Image, ImageGrab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import latex2sympy2
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.backends.backend_pdf
from sympy import symbols, preview, Symbol
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
plt.rcParams['toolbar'] = 'None'

title_Text = ''
page_number_var = 0
rowing = 250
qNum = 1
numebring = 0


class DragDropListbox(tk.Listbox):
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        self.bind("<ButtonPress-1>", self.onStart)
        self.bind("<B1-Motion>", self.onDrag)
        self.curIndex = None

    def onStart(self, event):
        self.curIndex = self.nearest(event.y)
    #reordering by dragging different files
    def onDrag(self, event):
        newIndex = self.nearest(event.y)
        if self.curIndex != newIndex:
            x = self.get(self.curIndex)
            self.delete(self.curIndex)
            self.insert(newIndex, x)
            self.curIndex = newIndex

#header default set to '' when done testing
HEADER = "header"
    
def save_fileList(): 
    savePath = tk.filedialog.asksaveasfilename(defaultextension=".kap", filetypes=[("KAP files", "*.kap")])
    savePath = open(savePath, 'w')
    for question in enumerate(file_list.get(0, tk.END)):
        #print(question[1])
        questSave = "(" + question[1] + "\n"
        print(questSave)
        savePath.write(questSave)
        
        
# Function to capture and save a copy of the canvas as a PDF
def save_canvas(): 
    global title_Text
    pdf_Name = title_Text + ".pdf"
    global HEADER
    headTrim = HEADER.replace('\n', '<br/>')
    global numebring
    
    #let user choose where to save the file
    savePath = tk.filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if savePath:
        pdf_Name = savePath
        copy_Save = canvas.Canvas(pdf_Name, pagesize=letter)

        #Setup the title
        width, height = letter
        tWidth = copy_Save.stringWidth(title_Text, "Helvetica-Bold", 24)
        tx = (width -tWidth) / 2
        copy_Save.setFont("Helvetica-Bold", 24)
        copy_Save.drawString(tx, 725, title_Text)
        
        #Setup the Header
        headStyle = ParagraphStyle('myStyle', fontName = 'Helvetica', fontSize=16, leading=20)
        copy_Save.setFont("Helvetica", 18)
        headPara = Paragraph(headTrim, headStyle)
        headPara.wrapOn(copy_Save, 700, 600)
        headPara.drawOn(copy_Save, width-575, height-160)

        #Setup for number of questions and getting their file names
        imNames = [item[3] for item in question_items]
        imNames = [imName + ".png" for imName in imNames]

    
        #Save the questions, maybe prompt user for questions per page
        qperpage = 2
        numPages = (len(imNames) + qperpage - 1) // qperpage
        for page in range(numPages):
            #print(page_number_var)
            #if(page_number_var.get() == 1):
                #print(page_number_var)
                #copy_Save.setFont("Helvetica", 12)
                #copy_Save.drawString(tx, 725, str(page))
            if (page > 0):
                copy_Save.showPage()
                x, y = 50, 670
            else:
                x, y = 50, 475

            # Draw the page number if enabled
            if(numebring == 1):
                page_number_text = f"Page {page + 1}"
                copy_Save.setFont("Helvetica", 12)
                copy_Save.drawString(width - 100, 30, page_number_text)  # Adjust position as needed

            for i in range(qperpage):
                index = page * qperpage + i
                if index < len(imNames):
                    imNam = imNames[index]
                    copy_Save.drawImage(imNam, x, y, width = 780, height = 130)
                    y-=250
                
        copy_Save.save()
    
#brings sidebar over
sidebar_frame = None
def setSidebar_frame(frame):
    global sidebar_frame
    sidebar_frame = frame

#brings root over
root = None
def setRoot(r):
    global root
    root = r

#brings sidebar2_canvas over
sidebar2_canvas = None
def setSidebar2_canvas(canvas):
    global sidebar2_canvas
    sidebar2_canvas = canvas

#brings file_list over
file_list = None
def setFile_list(fList):
    global file_list
    file_list = fList

#holds the questions to make deletion and updating easier
question_items = []

#Fixed so questions all fit on one line, but adds some uneeded lines, not sure how to fix
def open_file():
    filepath = tk.filedialog.askopenfilename()
    with open(filepath, "r") as fil:
        quest = []
        firstLine = False
        r = 0
        check = 0
        for ln in fil:
            if ln.startswith("\q") or ln.startswith("(") or ln.startswith(" ") or ln.startswith("$$"):
                if ln.startswith("\q"):
                    check = 1
                else:
                    check = 0
                if(ln.startswith(" ")):
                    if firstLine:
                        if quest:
                            quest[-1] += ln
                        else:
                            quest.append(ln[1:])
                elif(ln.startswith("(")):
                    rn = ln.strip()
                    rn = "(" + rn
                    quest.append(rn[1:])
                else:
                    quest.append(ln[1:])
                firstLine = True
            elif(check == 1):
                check = 0
                quest[-1] += ln
                
    #strip the uneeded characters
    ques = np.array(quest)
    que = np.char.replace(ques, ',', '')
    que = np.char.replace(ques, '\\\\', '')
    que = np.char.replace(que, '$', '')
    que = np.char.replace(que, '$$', '')
    que = np.char.replace(que, '%', '')
    que = np.char.replace(que, '\displaystyle', '')
    que = np.char.replace(que, "\n", '')
    que = np.char.replace(que, "\end{questions}", '')
    que = np.char.replace(que, "question", '')
    #que = np.char.strip(que)
    que = np.char.strip(que, '\\')

    

    #Add to List and display on canvas
    if filepath:
        i = 0
        global rowing 
        rowing = 250
        for x in que:
            file_list.insert(tk.END, x)
            display_Question(x, i, rowing)
            i= i+1
            rowing += 250
            #print(i)
        #print(question_items)
        footer_update()
        
# Method that sets up the title
def Get_Title(INPUT):
    sidebar2_canvas.delete("Title")
    global title_Text
    title_Text = INPUT
    #print (INPUT)
   # print (title_Text)
    sidebar2_canvas.create_text(800, 100 ,text=INPUT, fill="black", font=('Helvetica 24 bold'), tags=("Title"))

def GUI_update():
    #singular place to run updates to the canvas
    #use for inserting questions and other objects to canvas
    #print("update")
    footer_update()
    #get canvas width
    canvas_width = sidebar2_canvas.winfo_width()

    sidebar2_canvas.delete("Header")
    sidebar2_canvas.create_text(300, 150, anchor='n', text=HEADER, fill="black", font=('Helvetica 18'), tags=("Header"))


#deletes a question
def deleteQues():
    selected = file_list.curselection()
    if selected:
        # get the index
        selectedIn = int(selected[0])

        # Ensure selectedIn is within the range of question_items
        if selectedIn < len(question_items):
            # gets rid of the item in the list
            canvas_item, tag, space, _, _ = question_items.pop(selectedIn)
            # deletes the item in the listbox and updates the canvas
            file_list.delete(selectedIn)
            sidebar2_canvas.delete("Question")

            plt.close('all')
            rowing = 250
            global qNum
            qNum = 1
            # redraws the entire question list (Maybe not needed)
            for i, question in enumerate(file_list.get(0, tk.END)):
                display_Question(question, i, rowing)
                rowing += 250
        else:
            print("Selected index is out of range.")

    
def edit_header():
    # Create a new window
    header_window = Toplevel(root)
    header_window.title("Edit Header")
    header_window.geometry("450x250")

    
    page_number_var = IntVar()
    # Add widgets for adding their own name, class, and date
    Label(header_window, text="Header Content:").grid(row=1, column=0, padx=10, pady=5)
    header_content_text = tk.Text(header_window, height=5, width=30)  # Adjust height and width as needed
    header_content_text.grid(row=1, column=1, padx=10, pady=5)
    default_header = "Name:_____________ \n Course:____________ \n Date:______________"
    header_content_text.insert('1.0', default_header)
    
    # Checkbutton for page numbering
    
    Checkbutton(header_window, text="Add Page Numbering", variable=page_number_var, onvalue=1, offvalue=0).grid(row=4, columnspan=2, padx=10, pady=10)  
    btn_apply_changes = Button(header_window, text="Apply Changes", command = lambda: header_update(header_content_text.get("1.0","end-1c"), page_number_var.get()))    
    btn_apply_changes.grid(row=2, column=0, columnspan=2, pady=10)


def closing():
    plt.close('all')
    directory = os.getcwd()
    allImagesDel = os.listdir(directory)
    for filename in allImagesDel:
        if filename.endswith('.png'):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
    root.destroy()
    

#grabs header data and can be later used to store data, for now it udpates a global var for testing, CHANGE THIS LOL
def header_update(header_text, page_numbering):
    #print(header_text)
    #print(page_numbering)
    global HEADER
    global numebring
    numebring = page_numbering
    HEADER = header_text
    #sidebar2_canvas.create_text(800, 100 ,text=HEADER, fill="black", font=('Helvetica 24 bold'), tags=("Header"))
    GUI_update()            

def page_numbering():
    global numebring
    print(numebring)
    if(numebring == 1):
        # Define the number of questions per page
        questions_per_page = 2  # Example value, adjust as needed

        # Define page heights
        first_page_height = 750  
        other_page_height = 500   

        # Get the total number of questions
        total_questions = len(question_items)

        # Calculate the total number of pages
        total_pages = (total_questions + questions_per_page - 1) // questions_per_page

        # Remove any previous page numbers
        sidebar2_canvas.delete("page_number")

        # Add page numbers
        
        for page in range(1, total_pages + 1):
            # Calculate y_position for each page number
            if page == 1:
                y_position = first_page_height - 100
            else:
                y_position = first_page_height + (page - 1) * other_page_height - 100
            
            # Create page number text
            page_number_text = f"Page {page}"
            sidebar2_canvas.create_text( sidebar2_canvas.winfo_width() -50 , y_position, text=page_number_text, font=("Helvetica", 10), tags="page_number")

        # Update the canvas scroll region if necessary
        sidebar2_canvas.configure(scrollregion=sidebar2_canvas.bbox("all"))
    else:
        sidebar2_canvas.delete("page_number")

def footer_update():
    # Define the number of questions per page
    questions_per_page = 2  # Example value, adjust as needed

    # Define page heights
    first_page_height = 750  
    other_page_height = 500   

    # Get the total number of questions
    total_questions = len(question_items)

    # Calculate the total number of pages
    total_pages = (total_questions + questions_per_page - 1) // questions_per_page

    # Print or update the footer with the total number of pages
    print("Total Pages:", total_pages)

    # Remove any previous lines (if you want to redraw them)
    sidebar2_canvas.delete("page_line")

    # Draw a line for the first page
    if total_pages > 0:
        sidebar2_canvas.create_line(0, first_page_height, sidebar2_canvas.winfo_width(), first_page_height, fill="black", tags="page_line")

    # Draw lines to indicate the end of each subsequent page
    for page in range(2, total_pages + 1):
        y_position = first_page_height + (page - 2) * other_page_height
        sidebar2_canvas.create_line(0, y_position, sidebar2_canvas.winfo_width(), y_position, fill="black", tags="page_line")

    # Update the canvas scroll region if necessary
    sidebar2_canvas.configure(scrollregion=sidebar2_canvas.bbox("all"))

    page_numbering()



#replace the text in the list with new text
def replaceQues(change, new_spacing):
    selected = file_list.curselection()
    
    #get rid of newlines
    change = change.replace('\n', '')
    
    if selected:
        selectedIn = int(selected[0])

        #delte the listbox object and replace with new text
        file_list.delete(selectedIn)
        file_list.insert(selectedIn, change)
        
        #delete the plot on the canvas and replace it with new text
        #print(question_items)
        #canvas_item, tag, space, _, _ = question_items.pop(selectedIn)
        #question_items.insert(selectedIn, (change, 'Question', new_spacing, _, _))
        updateQuestions(selectedIn, change, new_spacing)
        #display_Question(change, selectedIn+1, new_spacing)

        
def edit_Question():
    # Create a new window
    question_win = Toplevel(root)
    question_win.title("Edit Question")
    question_win.geometry("650x300")
    
    #Edit Question Text (Now much bigger)
    p = Label(question_win, text = "Edit Question:").place(relx=0.5, rely=.2, anchor='s') 
    t = Text(question_win, height = 5, width = 80)
    t.place(relx=0.5, rely=0.5, anchor='s')
    t.insert(END, file_list.get(ANCHOR))
    
    #l = Label(question_win, text = "Edit Spacing:").place(relx=0.5, rely=.6, anchor='s') 
    #g = Text(question_win, height = 1, width = 8)
    #g.place(relx=0.5, rely=0.75, anchor='s')
    #g.insert(END, 20)
    
    def apply_and_close():
        replaceQues(t.get(1.0, END), 20)
        question_win.destroy()
        
    #Button to add the new text
    add_text_button = Button(question_win, text="Apply", command= apply_and_close)
    add_text_button.place(relx=0.5, rely=.9, anchor='s')   
    
    
def add_text():
    e = 'Sample Text'
    file_list.insert(tk.END, e)
    x = len(question_items)
    print(x)
    global rowing
    display_Question(e, x, rowing)

def display_Question(displ, row, spacing):
    global qNum
    #print(displ)
    if(displ.startswith(" ") or displ.startswith("[")):
        #displ = str(qNum) + ". " + displ
        #qNum += 1
        displ = displ.replace(' ', '\:')
    displ = "$" + displ + "$"
    print(displ)
    if row < len(question_items):
        previous_canvas, _, _2, _, _ = question_items[row]
        if isinstance(previous_canvas, FigureCanvasTkAgg):
            previous_canvas.get_tk_widget().get_tk_widget().destroy()
        question_items.pop(row)
        
    #sets up the size of the figure (Width, Height)
    fig = plt.figure(figsize=(12, 2))
    
    #sets up spacing between questions, need to make editable
    #dis_ques = FigureCanvasTkAgg(fig, master = sidebar2_canvas)
    if(row == 0):
        #first one needs more spacing so header and title can show, need to adjust incase first item is deleted
        spacing = 250
        y_pos = spacing * 1
    else:
        #print(spacing)
        y_pos = spacing * row

    #sets up the display area on the canvas
    #dis_ques.get_tk_widget().grid(row=row, column=1, sticky="nsew", pady = (y_pos, 0), padx = (125, 0))
       
    #Makes sure the canvas isn't going to resize
    sidebar2_canvas.grid_rowconfigure(row, weight=0)
    sidebar2_canvas.grid_columnconfigure(0, weight=0)
    #dis_ques.draw()
    
    #determines the text size and position, probably need to change the style
    text = fig.text(
        x=0,  # x-coordinate to place the text
        y=0.5,  # y-coordinate to place the text
        s=displ,
        horizontalalignment="left",
        verticalalignment="center",
        fontsize=12,
        fontdict={'family': 'monospace', 'color':  'black', 'weight': 'normal'}
    )
    
    #save the problems as pngs for later
    filnam = 'Question ' + str(row)
    fig.savefig(filnam)
    #print(filnam)
    img = PhotoImage(file=filnam+'.png')
    my_img = sidebar2_canvas.create_image(10, spacing, anchor=NW, image=img, tags = "Question")
    sidebar2_canvas.update()
    
    #puts the object in a list for safekeeping
    #canvasHold = dis_ques.get_tk_widget()
    question_items.insert(row, (displ, "Question", spacing, filnam, img))
    #print(spacing)
    #resize_canvas()
    

def resize_canvas():
    total_height = 0
    for _, _, spacing, _ in question_items:
        total_height += spacing
        
    #print(sidebar2_canvas.winfo_reqheight())
    sidebar2_canvas.configure(scroll=(0, 0, 0, total_height))
    #print(sidebar2_canvas.winfo_reqheight())
   
#WIP 
#def clear_questions():#
    #f#or canvas_item, _, _, _, _ in question_items:
        #print(canvas_item)
    #question_items.clear()

#updates the quesitons in the display, a little buggy but works if you play around with editing quesiton text
def updateQuestions(selectedIn, change, spacing):
    #sidebar2_canvas.delete('Question')
    cavnObj, tag, spac, nam, im = question_items.pop(selectedIn)
    
    display_Question(change, selectedIn, spacing)
    
    #plt.close('all')
    
    #redraws the entire question list
    #for i, question in enumerate(file_list.get(0, tk.END)):
    #   if(i >= file_list.size()):
     #       break
      #  display_Question(question, i, int(holding[i]))