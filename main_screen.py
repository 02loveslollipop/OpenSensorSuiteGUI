import tkinter as tk
from tkinter import ttk


class main_screen(ttk.Frame):
    def __init__(self, root):
        

        
        #lock the window size
        root.resizable(width=False, height=False)
        
        #change the title
        root.title("Open Sensor Suite")
        
        #Init the frame
        self.frame = ttk.Frame(root)
        self.frame.pack()
        
        #Init the label
        self.analaticsFrame = ttk.LabelFrame(self.frame, text="Analatics")
        self.analaticsFrame.grid(row=0, column=0,padx=5)
        
        #Label and entry avg 100
        self.avg100Label = ttk.Label(self.analaticsFrame, text="Avg 100")
        self.avg100Label.grid(row=0, column=0,pady=5)
        self.avg100Entry = ttk.Entry(self.analaticsFrame)
        self.avg100Entry.grid(row=0, column=1,pady=5)
        self.avg100Entry.config(state="readonly")
        
        #Label and entry standard deviation
        self.stdDevLabel = ttk.Label(self.analaticsFrame, text="Std Deviation")
        self.stdDevLabel.grid(row=1, column=0,pady=5)
        self.stdDevEntry = ttk.Entry(self.analaticsFrame)
        self.stdDevEntry.grid(row=1, column=1,pady=5)
        self.stdDevEntry.config(state="readonly")
        
        #other label frame called entry
        self.entryFrame = ttk.LabelFrame(self.frame, text="Entry")
        self.entryFrame.grid(row=0, column=1, padx=5)
        
        #Label and entry for the sensor id
        self.sensorIdLabel = ttk.Label(self.entryFrame, text="Sensor ID")
        self.sensorIdLabel.grid(row=0, column=0,pady=5)
        self.sensorIdEntry = ttk.Entry(self.entryFrame)
        self.sensorIdEntry.grid(row=0, column=1,pady=5)
        
        #Label and entry for the sensor value
        self.sensorValueLabel = ttk.Label(self.entryFrame, text="Sensor Value")
        self.sensorValueLabel.grid(row=1, column=0,pady=5)
        self.sensorValueEntry = ttk.Entry(self.entryFrame)
        self.sensorValueEntry.grid(row=1, column=1,pady=5)
        
        #frame for the buttons
        self.buttonFrame = ttk.Frame(self.entryFrame)
        self.buttonFrame.grid(row=2, column=0, columnspan=2)
        
        
        #Next entry and previous entry buttons inside the button frame
        self.nextButton = ttk.Button(self.buttonFrame, text="Next")
        self.nextButton.grid(row=2, column=1,padx=10)
        self.prevButton = ttk.Button(self.buttonFrame, text="Prev")
        self.prevButton.grid(row=2, column=0)
        
        #Button to update the entry centered on the bottom
        
        self.updateButton = ttk.Button(self.buttonFrame, text="Update")
        self.updateButton.grid(row=3, column=0, columnspan=2)
        
        #Button to delete the entry centered on the bottom
        self.deleteButton = ttk.Button(self.buttonFrame, text="Delete")
        self.deleteButton.grid(row=4, column=0, columnspan=2)
        
        #other label frame called 
        
        
        
    def on_button_click(self):
        self.label.config(text="Button Clicked!")

