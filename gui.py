import tkinter as tk
import query

class GUI:

    #Creates a tk object, a window title, and attributes related to I/O
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(0,0)
        self.root.title("Search Engine")
        self.output = tk.StringVar()
        self.errorMsg = tk.StringVar()

    #Creates the buttons and labels
    def createDisplay(self):
        self.createIO()
        self.createButtons()
        self.createErrorDisplay()
        self.createTitle()

    #Creates program name
    def createTitle(self):
        tk.Label(master = self.root, width = 10, text = "Search Engine").place(x = 360, y = 50)
        
    #Retrieves the statement typed and calls getOutput to verify if valid
    def getInput(self):
        string = self.textInput.get("1.0","end-1c")
        self.getOutput(string)

    #Verifies if given query is valid
    def getOutput(self,string):
        resultStr = query.processQuery(string)
        self.errorMsg.set("Done")
        self.setOutput(resultStr)

    #Clears the input field    
    def clearInput(self):
        self.textInput.delete("1.0","end-1c")

    #Clears the output field
    def clearOutput(self):
        self.output.set("")

    #Clears I/O fields
    def clearFields(self):
        self.clearInput()
        self.clearOutput()

    #Displays the search results
    def setOutput(self,returnValue):
        self.output.set(returnValue)

    #Creates a search button to submit queries
    def createSearchButton(self):
        tk.Button(master = self.root, width = 10, text = "Search", command = self.getInput).place(x = 360, y = 125)

    #Creates a clear button to clear fields
    def createClearButton(self):
        tk.Button(master = self.root, width = 10, text = "Clear", command = self.clearFields).place(x = 360, y = 175)

    #Creates the run and clear button
    def createButtons(self):
        self.createSearchButton()
        self.createClearButton()

    #Creates fields for inputting search query and receiving its results
    def createIO(self):
        self.textInput = tk.Text(master = self.root, width = 40, height = 20)
        self.textInput.grid(row = 0)
        tk.Label(master = self.root, wraplength = 800, bg = "light grey", width = 90, height = 21, textvariable = self.output).grid(row = 0, column = 300,sticky = "NE")

    #Creates a label for error displaying
    def createErrorDisplay(self):
        tk.Label(master = self.root, width = 20, bg = "light grey", textvariable = self.errorMsg).grid(row = 5, column = 55)

    #Runs the program
    def run(self):
        self.root.mainloop()
