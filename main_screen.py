import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import queue
import threading
import redis as rd
import time
from config import config
import datetime

class main_screen(ttk.Frame):
    
    def __init__(self, root, conf: config) -> None:
        
        self.root = root
        self.conf = conf
        self.graphDataX = np.linspace(0, 1, conf.graph_history)
        self.graphDataY = np.sin(self.graphDataX)
        self.index = -1
        self.current_index_posix_time = 0
        
        #handle the window close event
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        #set icon to favicon.ico
        self.root.iconbitmap('favicon.ico')
        
        #lock the window size
        self.root.resizable(width=False, height=False)
        
        #change the title
        self.root.title("Open Sensor Suite")
        
        #Init the frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack()
        
        #Init the label
        self.analaticsFrame = ttk.LabelFrame(self.frame, text="Analatics (last 100))")
        self.analaticsFrame.grid(row=0, column=0,padx=5)
        
        #Label and entry avg 100
        self.avg100Label = ttk.Label(self.analaticsFrame, text="Avg")
        self.avg100Label.grid(row=0, column=0,pady=5)
        self.avg100Entry = ttk.Entry(self.analaticsFrame)
        self.avg100Entry.grid(row=0, column=1,pady=5,padx=5)
        self.avg100Entry.config(state="readonly")
        
        #Label and entry standard deviation
        self.stdDevLabel = ttk.Label(self.analaticsFrame, text="Std Dev")
        self.stdDevLabel.grid(row=1, column=0,pady=5)
        self.stdDevEntry = ttk.Entry(self.analaticsFrame)
        self.stdDevEntry.grid(row=1, column=1,pady=5,padx=5)
        self.stdDevEntry.config(state="readonly")
        
        #other label frame called entry
        self.entryFrame = ttk.LabelFrame(self.frame, text="Entry")
        self.entryFrame.grid(row=0, column=1, padx=5)
        
        #label and entry for index of the entry (not editable)
        self.indexLabel = ttk.Label(self.entryFrame, text="Index")
        self.indexLabel.grid(row=0, column=0,pady=5)
        self.indexEntry = ttk.Entry(self.entryFrame)
        self.indexEntry.grid(row=0, column=1,pady=5,padx=5)
        self.indexEntry.insert(0, self.index)
        self.indexEntry.config(state="readonly")
        
        #Label and entry for the sensor date
        self.sensorDateLabel = ttk.Label(self.entryFrame, text="Date")
        self.sensorDateLabel.grid(row=1, column=0,pady=5)
        self.sensorDateEntry = ttk.Entry(self.entryFrame)
        self.sensorDateEntry.grid(row=1, column=1,pady=5,padx=5)
        self.sensorDateEntry.config(state="readonly")
        
        #Label and entry for the sensor value
        self.sensorValueLabel = ttk.Label(self.entryFrame, text="Value")
        self.sensorValueLabel.grid(row=2, column=0,pady=5)
        self.sensorValueEntry = ttk.Entry(self.entryFrame)
        self.sensorValueEntry.grid(row=2, column=1,pady=5,padx=5)
        
        #update values with redis data
        self.next()
        
        #frame for the buttons
        self.buttonFrame = ttk.Frame(self.entryFrame)
        self.buttonFrame.grid(row=3, column=0, columnspan=2)
        
        
        #Next entry and previous entry
        self.nextButton = ttk.Button(self.buttonFrame, text="Next", command=self.next)
        self.nextButton.grid(row=2, column=1,padx=10,pady=5)
        self.prevButton = ttk.Button(self.buttonFrame, text="Prev", command=self.prev)
        self.prevButton.grid(row=2, column=0,padx=10,pady=5)
        
        #update entry
        self.updateButton = ttk.Button(self.buttonFrame, text="Update",command=self.update)
        self.updateButton.grid(row=3, column=0, columnspan=2,pady=5)
        
        #delete entry
        self.deleteButton = ttk.Button(self.buttonFrame, text="Delete", command=self.delete)
        self.deleteButton.grid(row=4, column=0, columnspan=2,pady=5)
        
        #other label frame called graph below and centered
        self.graphFrame = ttk.LabelFrame(self.frame, text="Graph")
        self.graphFrame.grid(row=1, column=0, columnspan=2)
        
        #init the figure
        self.figure, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.plot, = self.ax.plot(self.graphDataX, self.graphDataY)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graphFrame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        #change the colors
        self.ax.set_facecolor('#1c1c1c')
        self.figure.set_facecolor('#1c1c1c')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        
        #change the texts
        self.ax.set_title("Sensor Data")
        self.ax.set_ylabel("Value")

        #animation
        self.animation = FuncAnimation(self.figure, self.update_plot, interval=self.conf.graph_time)
        
        #thread
        self.dataQueue = queue.Queue()
        self.thread = threading.Thread(target=self.async_data_update)
        self.thread.daemon = True
        self.thread.start()
        
    def on_closing(self):
        self.root.destroy()
        exit()
        
    def next(self):
        connection = self.redis_connect()
        self.index += 1
        result = connection.zrange('sensor1', self.index, self.index, withscores=True)
        if result == []:
            self.index -= 1
            return
        value = result[0][0]
        self.current_index_posix_time = float(result[0][1])
        date = datetime.datetime.fromtimestamp(self.current_index_posix_time).strftime('%Y-%m-%d %H:%M:%S')
        self.sensorDateEntry.config(state="normal")
        self.indexEntry.config(state="normal")
        self.sensorDateEntry.delete(0, tk.END)
        self.sensorValueEntry.delete(0, tk.END)
        self.indexEntry.delete(0, tk.END)
        self.sensorDateEntry.insert(0, date)
        self.sensorValueEntry.insert(0, value)
        self.indexEntry.insert(0, self.index)
        self.indexEntry.config(state="readonly")
        self.sensorDateEntry.config(state="readonly")
        
    def prev(self):
        connection = self.redis_connect()
        self.index -= 1
        result = connection.zrange('sensor1', self.index, self.index, withscores=True)
        if result == []:
            self.index += 1
            return
        value = result[0][0]
        date = datetime.datetime.fromtimestamp(self.current_index_posix_time).strftime('%Y-%m-%d %H:%M:%S')
        self.sensorDateEntry.config(state="normal")
        self.indexEntry.config(state="normal")
        self.sensorDateEntry.delete(0, tk.END)
        self.sensorValueEntry.delete(0, tk.END)
        self.indexEntry.delete(0, tk.END)
        self.sensorDateEntry.insert(0, date)
        self.sensorValueEntry.insert(0, value)
        self.indexEntry.insert(0, self.index)
        self.indexEntry.config(state="readonly")
        self.sensorDateEntry.config(state="readonly")
    
    def update(self):
        connection = self.redis_connect()
        try:
            value = float(self.sensorValueEntry.get())
        except ValueError:
            return
        connection.zremrangebyrank('sensor1', self.index, self.index)
        connection.zadd('sensor1', {value: self.current_index_posix_time})
        
    def delete(self):
        connection = self.redis_connect()
        connection.zremrangebyrank('sensor1', self.index, self.index)
        self.next()
        
    def redis_connect(self) -> rd.Redis:
        connect = rd.Redis(host=self.conf.host, port=self.conf.port, password=self.conf.password)
        return connect
    
    def update_plot(self,framedata):
        try:
            #update the data from the queue
            self.graphDataY = self.dataQueue.get_nowait()
            
            # Update the plot
            self.plot.set_ydata(self.graphDataY)
            self.ax.set_ylim(min(self.graphDataY), max(self.graphDataY))
            self.canvas.draw()
            
            #update the avg100 and stdDev
            self.avg100Entry.config(state="normal")
            self.avg100Entry.delete(0, tk.END)
            self.avg100Entry.insert(0, np.average(self.graphDataY))
            self.avg100Entry.config(state="readonly")
            self.stdDevEntry.config(state="normal")
            self.stdDevEntry.delete(0, tk.END)
            self.stdDevEntry.insert(0, np.std(self.graphDataY))
            self.stdDevEntry.config(state="readonly")
        
        except queue.Empty:
            pass     
        
    def async_data_update(self):
        
        connect = self.redis_connect()
        
        n=self.conf.graph_history
        query_amount = n-1
        
        while True:
            response = connect.zrevrange('sensor1', 0, query_amount, withscores=True)
            i = 0
            new_GraphDataY = np.zeros(len(response))
        
            for reading in response:
                new_GraphDataY[i] = reading[0]
                i += 1
                            
            #Push the data to the queue
            self.dataQueue.put(new_GraphDataY)
            
            #Schedule the next update
            time.sleep(self.conf.graph_time/1000)
            

