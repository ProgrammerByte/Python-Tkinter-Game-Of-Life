from tkinter import *
from copy import copy

def onclick(self):
    global colour
    if self["bg"] == "Yellow":
        self["bg"] = "Black"
    else:
        self["bg"] = "Yellow"

def Open(root2):
    openwindow = Tk()
    openwindow.title("Open")
    openwindow.grid()

    inputlabel = Label(openwindow, text = "Name of file:").grid(row = 1, column = 1)
    nameinput = Entry(openwindow)
    nameinput.grid(row = 1, column = 2)

    confirmbutton = Button(openwindow, text = "Open", command = lambda: openfile(nameinput, root2, openwindow))
    confirmbutton.grid(row = 2, column = 2)

def openfile(nameinput, root2, openwindow):
    try:
        filetoread = open(nameinput.get() + ".txt", "r")
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found! Please enter the name of a compatible text file")

    else:
        contents = filetoread.read()
        contents = contents.split()
        filetoread.close()
        verf = "Y"
        if len(contents) >= 2:
        
            if contents[0].isdigit() and contents[1].isdigit(): #This part of the program verifies that the file is compatible
                for i in range(len(contents) - 2):
                    
                    if i % 2 == 0:
                        if contents[i + 2].isdigit():
                            pass
                        else:
                            print("Herre")
                            verf = "N"

                    else:
                        inlist = "N"
                        if contents[i + 2] != "Black" and contents[i + 2] != "Yellow":
                            verf = "N"
                            
            else:
                verf = "N"


        else:
            verf = "N"

        if verf == "N":
            messagebox.showerror("Invalid Format", "File is formatted incorrectly and cannot be opened")

        else:
            newfile = "N"
            height = int(contents[0])
            width = int(contents[1])
            buildgrid(height, width, newfile, contents, openwindow, root2)

def saveas(buttonslist, height, width):
    savewindow = Tk()
    savewindow.title("Save As")
    savewindow.grid()

    inputlabel = Label(savewindow, text = "Name of new file:").grid(row = 1, column = 1)
    nameinput = Entry(savewindow)
    nameinput.grid(row = 1, column = 2)

    confirmbutton = Button(savewindow, text = "Save as", command = lambda: createfile(buttonslist, nameinput, height, width, savewindow))
    confirmbutton.grid(row = 2, column = 2)

    savewindow.mainloop()

def createfile(buttonslist, nameinput, height, width, savewindow):
    Clear = open(nameinput.get() + ".txt", "w")
    Clear.close()

    append = open(nameinput.get() + ".txt", "a+")
    append.write(height + " " + width)

    appendarray = list()
    for i in range(len(buttonslist)):
        for x in range(len(buttonslist[i])):
            appendarray.append(buttonslist[i][x]["bg"])

    completed = "N"
    repeated = 1
    finalappendarray = list()
    for i in range(len(appendarray) - 1):
        if appendarray[i] == appendarray[i + 1]:
            repeated = repeated + 1
        else:
            finalappendarray.append(repeated)
            finalappendarray.append(appendarray[i])
            repeated = 1

    finalappendarray.append(repeated)
    finalappendarray.append(appendarray[i + 1])

    for i in range(len(finalappendarray)):
        append.write(" " + str(finalappendarray[i]))
        
    append.close()
    savewindow.destroy()

def Run(buttonslist):
    class GameofLife():
        def __init__(s, buttonslist):
            s.root = Tk()
            s.root.title("GameOfLife")
            s.root.grid()

            s.cellcolours = buttonslist
            s.height = len(s.cellcolours)
            s.width = len(s.cellcolours[0])

            s.maingrid = list()
            for i in range(s.height):
                s.maingrid.append([])
                for x in range(s.width):
                    s.maingrid[i].append("")
                    s.maingrid[i][x] = Label(s.root, height = 1, width = 2, bg = s.cellcolours[i][x]["bg"])
                    s.maingrid[i][x].grid(row = i, column = x)


            GameofLife.RefreshScreen(s)
            s.root.mainloop()

        def RefreshScreen(s):
            dead = list()
            births = list()
            s.combinationsi = [1, -1, 0, 0, 1, 1, -1, -1]
            s.combinationsx = [0, 0, 1, -1, 1, -1, 1, -1] #All the surrounding spaces

            for i in range(s.height):
                for x in range(s.width):
                    neighbours = 0
                    for combinations in range(8):
                        icoord = (i + copy(s.combinationsi[combinations])) % s.height
                        xcoord = (x + copy(s.combinationsx[combinations])) % s.width
                        if s.maingrid[icoord][xcoord]["bg"] == "Yellow":
                            neighbours += 1

                    if neighbours == 3 and s.maingrid[i][x]["bg"] == "Black":
                        births.append([i, x])

                    elif (neighbours == 1 or neighbours == 0) and s.maingrid[i][x]["bg"] == "Yellow":
                        dead.append([i, x])

                    elif neighbours >= 4 and s.maingrid[i][x]["bg"] == "Yellow":
                        dead.append([i, x])

            for z in range(len(dead)):
                i = dead[z][0]
                x = dead[z][1]
                s.maingrid[i][x].configure(bg = "Black")

            for z in range(len(births)):
                i = births[z][0]
                x = births[z][1]
                s.maingrid[i][x].configure(bg = "Yellow")

            s.root.after(300, GameofLife.RefreshScreen, s)
                    

    game = GameofLife(buttonslist)

def buildgrid(height, width, newfile, contents, openwindow, root2):
    decompressedcontents = list()

    if newfile == "N":
        for i in range(len(contents) - 2):
            if contents[i + 2].isdigit():
                for x in range(int(contents[i + 2])):
                   decompressedcontents.append(contents[i + 3])
    
    root = Tk()
    root.title("Canvas")
    root.grid()

    menu = Menu(root)
    root.config(menu = menu)
    filemenu = Menu(menu) #This part creates the menu
    menu.add_cascade(label = "File", menu = filemenu)
    
    filemenu.add_command(label = "Open", command = lambda: Open(buttonslist))
    filemenu.add_command(label = "New", command = lambda: setup())
    filemenu.add_command(label = "Save As", command = lambda: saveas(buttonslist, height, width))

    menu.add_cascade(label = "Run", command = lambda: Run(buttonslist))

    buttonslist = list()

    cleanser = Frame(root)
    
    for i in range(int(height)):
        buttonslist.append([])
        
        for x in range(int(width)):
            buttonslist[i].append("")
            buttonslist[i][x] = Button(cleanser, bg = "Black",width = 2, height = 1, command = lambda i=i, x=x: onclick(buttonslist[i][x]))
            if newfile == "N":
                temp = i * width
                temp = temp + x
                
                buttonslist[i][x]["bg"] = decompressedcontents[temp]
            buttonslist[i][x].grid(row = i, column = x)

    cleanser.grid(row = 1, column = 1)

    placeholderlabel = Label(root, text = "").grid(row = 2)

    if newfile == "N":
        openwindow.destroy()

    if root2 != 0:
        root2.destroy()

def verification(heightentry, widthentry, setupwindow):
    width = widthentry.get()
    height = heightentry.get()
    newfile = "Y"
    openwindow = 0
    root2 = 0
    contents = list()
    
    if width.isdigit() and height.isdigit():
        if int(width) <= 80 and int(height) <= 35 and int(width) >= 2 and int(height) >= 2:
            setupwindow.destroy()
            buildgrid(height, width, newfile, contents, openwindow, root2)

        else:
            messagebox.showerror("Invalid", "Width must be between 2 and 80 and height must be between 2 and 35")

    else:
        messagebox.showerror("Invalid", "Width and Height must be integers!")


def setup():
    setupwindow = Tk()
    setupwindow.title("Setup")
    setupwindow.grid()

    menu = Menu(setupwindow)
    setupwindow.config(menu = menu)
    filemenu = Menu(menu) #This part creates the menu
    menu.add_cascade(label = "File", menu = filemenu)
    
    filemenu.add_command(label = "Open", command = lambda: Open(setupwindow))
    
    heightlabel = Label(setupwindow, text = "       Height:       ").grid(row = 1, column = 1)
    heightentry = Entry(setupwindow)
    heightentry.grid(row = 1, column = 2)

    widthlabel = Label(setupwindow, text = "       Width:       ").grid(row = 2, column = 1)
    widthentry = Entry(setupwindow)
    widthentry.grid(row = 2, column = 2)

    nextbutton = Button(setupwindow, text = "Continue", command = lambda: verification(heightentry, widthentry, setupwindow)).grid(row = 4, column = 2)

    setupwindow.mainloop()

if __name__ == "__main__":
    setup()
    quit()

