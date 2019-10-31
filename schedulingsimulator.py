from tkinter import *
import numpy as np
import pandas as pd
import operator
import tkinter.ttk as tkt
import queue
import matplotlib.pyplot as plt

class ganttInput():
    def __init__(self) :
        self.num = 0
        self.start = 0
        self.fin = 0

class dataInput:
    def __init__(self) :
        self.num = 0 # Process ID
        self.ar = 0 # Arrival time
        self.bt = 0 # Burst time
        self.wt = 0 # Wait time
        self.tat = 0 # Turn around time
        self.serv = 0 # Service time
        self.fint = 0 # Finish/Completion time
        self.prio = 0 # Priority
        self.rem_bt = 0 # Remaining burst time
        self.started = False # Boolean for process added to queue

class MyFirstGUI:

    def __init__(self, master):
        self.master = master
        master.title("Scheduling Visualiser")

        self.totalP = 0
        self.dat = []
        self.wt = []
        self.tat = []
        self.FINALT = 0
        self.ganttP = []
        self.ganttT = []
        self.firstarr = 0
        self.colors = ['red', 'blue', 'green', 'orange', 'yellow', 'navy', 'purple', 'pink', 'slategrey', 'darkcyan']

        self.frame1 = Frame(master, bd=3, relief=RAISED, height=500, width=550)
        self.frame1.grid(row=1, column=1,sticky=N+S+E+W)

        self.frame2 = Frame(master, bd=3, relief=RIDGE, height=500, width=500)
        self.frame2.grid(row=1, column=2,sticky=N+S+E+W)

        self.frame3 = Frame(master, bd=3, relief=RAISED, height=100, width=550)
        self.frame3.grid(row=2, column=1,sticky=N+S+E+W)

        self.frame4 = Frame(master, bd=3, relief=RIDGE, height=300, width=500)
        self.frame4.grid(row=2, column=2,sticky=N+S+E+W)

        self.ORDERLabel = Label(self.frame3, text="Waiting and Turn-Around Times",font=("arial", 15), width=27,relief=SUNKEN)
        self.ORDERLabel.grid(row=0, column=0)
        self.tree1 = tkt.Treeview(self.frame3, height=10)
        self.tree1["columns"]=("waiting","service","turnat")
        self.tree1.column("#0", width=130, minwidth=130 , stretch=NO)
        self.tree1.column("waiting", width=130, minwidth=130, stretch=NO)
        self.tree1.column("service", width=130, minwidth=130)
        self.tree1.column("turnat", width=130, minwidth=130)
        self.tree1.heading("#0",text="Process No.",anchor=W)
        self.tree1.heading("waiting", text="Waiting Time",anchor=W)
        self.tree1.heading("service", text="Completion Time",anchor=W)
        self.tree1.heading("turnat", text="Turn Around Time",anchor=W)
        self.tree1.grid(row=2, padx=50, pady=10) 

        #self.lab1 = Label(self.frame2, text="Process Name").grid(row=1, column=1)
        #self.lab2 = Label(self.frame2, text="Arrival Time").grid(row=1, column=2)
        #self.lab3 = Label(self.frame2, text="Waiting Time").grid(row=1, column=3)
        self.INPUTLabel = Label(self.frame1, text="Input Data",font=("arial", 15), width=15,relief=SUNKEN)
        self.INPUTLabel.grid(row=0, column=0)
        self.rows = []
        for i in range(1,13):
            cols = []
            if(i == 1) : 
                e = Label(self.frame1, text="Process",font=("serif", 12), width=15,relief=RAISED, anchor=W)
                e.grid(row=i, column=0, sticky=NSEW, padx=10,pady=5)
                e = Label(self.frame1, text="Arrival Time",font=("serif", 12), width=15,relief=RAISED, anchor=W)
                e.grid(row=i, column=1, sticky=NSEW, padx=10,pady=5)
                e = Label(self.frame1, text="Burst Time",font=("serif", 12), width=15,relief=RAISED, anchor=W)
                e.grid(row=i, column=2, sticky=NSEW, padx=10,pady=5)
                self.prioLabel = Label(self.frame1, text="Priority",font=("serif", 12), width=15,relief=RAISED, anchor=W)
                self.prioLabel.grid(row=i, column=3, sticky=NSEW, padx=10,pady=5)
                self.prioLabel.grid_remove()
            elif( i==12 ):
                for j in range(4):
                    e = Label(self.frame1, text="",font=("serif", 7), width=15, anchor=W)
                    e.grid(row=i, column=j, sticky=NSEW,padx=10)
            else:
                for j in range(4):
                    e = Entry(self.frame1,font=("Times New Roman", 12),width=15,relief=RIDGE)
                    e.grid(row=i, column=j, sticky=NSEW,padx=10)
                    if( j == 3 ) :
                        e.grid_remove()
                    cols.append(e)
                self.rows.append(cols)

        self.DATALabel = Label(self.frame2, text="Parameters",font=("arial", 25), width=10,relief=SUNKEN)
        self.DATALabel.grid(row=0, column=0)
        self.algoLabel = Label(self.frame2, text="Choose the scheduling algorithm",font=("Times New Roman", 12), width=25)
        self.algoLabel.grid(row=1, column=0, pady=5)
        self.algolist = tkt.Combobox(self.frame2, 
                            values=[
                                    "FCFS", 
                                    "SJF",
                                    "SRTF",
                                    "Priority",
                                    "Priority(Pre-emption)",
                                    "Round Robin"])
        self.algolist.grid(row=2, column=0)
        self.algolist.current(0)
        self.algolist.bind("<<ComboboxSelected>>", self.callbackFunc)

        self.quantLabel = Label(self.frame2, text="Quantum Time:",font=("serif", 10), width=7,relief=RAISED, anchor=W)
        self.quantLabel.grid(row=2, column=1, sticky=NSEW)
        self.quant = Entry(self.frame2, font=("Times New Roman", 13),width=6,relief=RIDGE)
        self.quant.grid(row=2, column=2, sticky=NSEW, padx=5)

        self.quant.grid_remove()
        self.quantLabel.grid_remove()

        self.addbutton = Button(self.frame2, text="SIMULATE", width=10, command=self.collect_data)
        self.addbutton.config(font=("arial", 20))
        self.addbutton.grid(row=3, column=0, pady=30)

        self.ResultsLabel = Label(self.frame4, text="Results",font=("arial", 25), width=10,relief=SUNKEN)
        self.ResultsLabel.grid(row=0, column=0)
        self.AvgWTLabel = Label(self.frame4, text="        Average Waiting Time :",font=("arial", 14), width=1, anchor=W)
        self.AvgWTLabel.grid(row=1, column=0, sticky=NSEW, padx=10,pady=15)

        self.AvgWTValue = Label(self.frame4, text="NaN",font=("arial", 14), width=10,relief=RIDGE, anchor=W)
        self.AvgWTValue.grid(row=1, column=1, sticky=NSEW,pady=15)

        self.AvgTATLabel = Label(self.frame4, text="Average Turn-Around Time :",font=("arial", 14), width=25, anchor=W)
        self.AvgTATLabel.grid(row=2, column=0, sticky=NSEW, padx=10,pady=10)

        self.AvgTATValue = Label(self.frame4, text="NaN",font=("arial", 14), width=10,relief=RIDGE, anchor=W)
        self.AvgTATValue.grid(row=2, column=1, sticky=NSEW,pady=10)

        self.addbutton = Button(self.frame4, text="View Gantt Chart", width=15, command=self.view_gantt)
        self.addbutton.config(font=("arial", 16))
        self.addbutton.grid(row=3, column=0, padx=20, pady=15)

    def view_gantt(self) :
        colors = self.colors[0:self.totalP]
        fig, ax = plt.subplots(figsize=(9.2, 3))
        ax.invert_yaxis()
        ax.set_xlim(0, self.FINALT)
        plt.xticks(np.arange(0, self.FINALT+1, 1))
        chartname = self.algolist.get()
        for i in range(len(self.ganttP)) :
            if( i==0 ) :
                ax.barh(chartname, self.ganttT[i], left=self.firstarr, height=0.5, label=chartname, color=colors[int(self.ganttP[i].num)-1] )
                ax.text(self.firstarr + 0.5, chartname, str(self.ganttP[i].num), ha='center', va='center',color='black')
            else :
                for x in self.ganttP:
                    print(x.num)
                ax.barh(chartname, self.ganttT[i], left=self.ganttP[i].start, height=0.5, label=chartname, color=colors[int(self.ganttP[i].num)-1] )
                ax.text(self.ganttP[i].start + 0.5, chartname, str(self.ganttP[i].num), ha='center', va='center',color='black')
        plt.show()

    def callbackFunc(self, event):
        if( self.algolist.get() =="Priority" or self.algolist.get() =="Priority(Pre-emption)" ) :
            self.prioLabel.grid()
            for row in self.rows :
                row[3].grid()
            self.quant.grid_remove()
            self.quantLabel.grid_remove()
        elif( self.algolist.get() =="Round Robin" ) :
            self.prioLabel.grid_remove()
            for row in self.rows :
                row[3].grid_remove()
            self.quant.grid()
            self.quantLabel.grid()
        else :
            self.prioLabel.grid_remove()
            for row in self.rows :
                row[3].grid_remove()
            self.quant.grid_remove()
            self.quantLabel.grid_remove()

    def FCFS(self) :
        self.dat.sort(key=operator.attrgetter('ar'))
        for i in self.tree1.get_children():
            self.tree1.delete(i)
        ginput = ganttInput()
        t = self.dat[0].ar
        ginput.start = t
        t += self.dat[0].bt
        ginput.fin = t
        # Wait and Turn Around Time Calculation
        self.dat[0].wt = 0
        self.dat[0].serv = 0
        self.dat[0].fint = t
        self.dat[0].tat = (self.dat[0].bt + self.dat[0].wt)
        ginput.num = self.dat[0].num 
        self.ganttP.append(ginput)
        self.ganttT.append(ginput.fin - ginput.start)
        self.firstarr = self.dat[0].ar
        self.tree1.insert("", 0, text=str(self.dat[0].num), values=(str(self.dat[0].wt),
                                                                    str(self.dat[0].fint),
                                                                    str(self.dat[0].tat)))                                                          
        for i in range(1, self.totalP) :
            ginput = ganttInput()
            if( self.dat[i].ar > t) :
                t = self.dat[i].ar
            old_t = t
            ginput.start = old_t
            t += self.dat[i].bt
            ginput.fin = t
            ginput.num = self.dat[i].num
            self.dat[i].serv = self.dat[i-1].serv + self.dat[i-1].bt 
            self.dat[i].fint = t
            self.dat[i].wt =  self.dat[i-1].fint - self.dat[i].ar 
            if( self.dat[i].wt < 0 ) :
                self.dat[i].wt = 0
            self.dat[i].tat =  self.dat[i].bt + self.dat[i].wt
            self.ganttP.append(ginput)
            self.ganttT.append(t-old_t)
            self.tree1.insert("", i, text=str(self.dat[i].num), values=(str(self.dat[i].wt),
                                                                    str(self.dat[i].fint),
                                                                    str(self.dat[i].tat)))
        self.FINALT = t
        self.ORDERLabel = Label(self.frame3, text="(Note : Processes are in order of execution)",font=("arial", 10), width=30)
        self.ORDERLabel.grid(row=1, column=0, padx=0)
        
    
    def SJF(self) :
        self.dat = sorted(self.dat, key=operator.attrgetter('bt'))
        self.dat = sorted(self.dat, key=operator.attrgetter('ar'))
        plist = []
        plist.append(self.dat[0])
        t = self.dat[0].ar
        self.dat[0].started = True 
        self.dat[0].wt = 0
        self.dat[0].serv = 0
        self.dat[0].tat = self.dat[0].wt + self.dat[0].bt
        self.firstarr = self.dat[0].ar
        completed = 0
        completelist = []
        while( completed != self.totalP ) :
            ginput = ganttInput()
            current_process = plist[0]
            old_t = t
            ginput.start = old_t
            t += current_process.bt
            ginput.fin = t
            ginput.num = current_process.num
            current_process.fint = t
            completed += 1
            self.ganttP.append(ginput)
            self.ganttT.append(t - old_t)
            plist.remove(current_process)
            completelist.append(current_process)
            flag = False
            for data in self.dat : 
                if( data != current_process and data.ar <= t and data.started == False ) :
                    plist.append(data)
                    data.started = True
                    flag = True
            if( flag == False and not plist and completed != self.totalP) :
                flag2 = False
                while( flag2 == False ) :
                    t += 1
                    print(t)
                    for data in self.dat :
                        if( data.ar <= t and data.started == False ) :
                            plist.append(data)
                            data.started = True
                            flag2 = True
            plist.sort(key=operator.attrgetter('bt'))
        self.FINALT = t
        for i in self.tree1.get_children():
            self.tree1.delete(i)

        self.tree1.insert("", 0, text=str(self.dat[0].num), values=(str(self.dat[0].wt),
                                                                    str(self.dat[0].fint),
                                                                    str(self.dat[0].tat)))
        for i in range(1, self.totalP):
            completelist[i].serv = completelist[i-1].serv + completelist[i-1].bt 
            completelist[i].wt =  completelist[i-1].fint - completelist[i].ar 
            if( completelist[i].wt < 0 ) :
                completelist[i].wt = 0
            completelist[i].tat =  completelist[i].bt + completelist[i].wt
            self.tree1.insert("", i, text=str(completelist[i].num), values=(str(completelist[i].wt),
                                                                            str(completelist[i].fint),
                                                                            str(completelist[i].tat)))
        self.ORDERLabel = Label(self.frame3, text="(Note : Processes are in order of execution)",font=("arial", 10), width=30)
        self.ORDERLabel.grid(row=1, column=0, padx=0)
            


    def SRTF(self): 
        self.ORDERLabel = Label(self.frame3, text="(Note : Processes are in order of completion)",font=("arial", 10), width=33)
        self.ORDERLabel.grid(row=1, column=0, padx=0)
        self.tree1.heading("service", text="Completion Time",anchor=W)
        self.dat = sorted(self.dat, key=operator.attrgetter('ar'))

        # Remaining time = burst time
        for data in self.dat :
            data.rem_bt = data.bt
        complete = 0
        t = 0
        minm = 999999999 # Sentinel value
        short = 0
        check = False

        while (complete != self.totalP):
            
            # Find out which process has minimum remaining time
            for j in range(self.totalP): 
                if ((self.dat[j].ar <= t) and                       # If arrival time less than T
                    (self.dat[j].rem_bt < minm) and self.dat[j].rem_bt > 0):# and remaining time less than 
                    minm = self.dat[j].rem_bt                          # minimum but greater than 0
                    short = j            # Set that process as first to schedule
                    check = True

            if (check == False): 
                t += 1
                continue

            ginput = ganttInput()
            ginput.start = t
            self.dat[short].rem_bt -= 1
            ginput.num = self.dat[short].num
    
            minm = self.dat[short].rem_bt
            if (minm == 0):  
                minm = 999999999
    
            if (self.dat[short].rem_bt == 0):  
    
                complete += 1
                check = False
      
                self.dat[short].fint = t + 1

                self.dat[short].wt = self.dat[short].fint - self.dat[short].ar - self.dat[short].bt

                if (self.dat[short].wt < 0): 
                    self.dat[short].wt = 0
            
            t += 1
            ginput.fin = t
            self.ganttP.append(ginput)
            self.ganttT.append(1)
        
        self.FINALT = t
        for data in self.dat :
            data.tat = data.wt + data.bt

        self.dat.sort(key=operator.attrgetter('fint'))
        for i in self.tree1.get_children():
            self.tree1.delete(i)

        for i in range(self.totalP) :
            self.tree1.insert("", i, text=str(self.dat[i].num), values=(str(self.dat[i].wt),
                                                                    str(self.dat[i].fint),
                                                                    str(self.dat[i].tat)))
        
    def Prior(self) :
        self.dat = sorted(self.dat, key=operator.attrgetter('prio'), reverse=True)
        self.dat = sorted(self.dat, key=operator.attrgetter('ar'))

        plist = []
        plist.append(self.dat[0])
        t = self.dat[0].ar
        self.dat[0].started = True 
        self.dat[0].wt = 0
        self.dat[0].serv = 0
        self.dat[0].tat = self.dat[0].wt + self.dat[0].bt
        completed = 0
        completelist = []
        while( completed != self.totalP ) :
            ginput = ganttInput()
            current_process = plist[0]
            old_t = t
            ginput.start = old_t
            t += current_process.bt
            ginput.fin = t
            current_process.fint = t
            completed += 1
            ginput.num = current_process.num
            self.ganttP.append(ginput)
            self.ganttT.append(t - old_t)
            plist.remove(current_process)
            completelist.append(current_process)
            flag = False
            for data in self.dat : 
                if( data != current_process and data.ar <= t and data.started == False ) :
                    plist.append(data)
                    data.started = True
                    flag = True
            if( flag == False and not plist and completed != self.totalP) :
                flag2 = False
                while( flag2 == False ) :
                    t += 1
                    print(t)
                    for data in self.dat :
                        if( data.ar <= t and data.started == False ) :
                            plist.append(data)
                            data.started = True
                            flag2 = True
            plist.sort(key=operator.attrgetter('prio'), reverse=True)
        
        self.FINALT = t
        for i in self.tree1.get_children():
            self.tree1.delete(i)

        self.tree1.insert("", 0, text=str(self.dat[0].num), values=(str(self.dat[0].wt),
                                                                    str(self.dat[0].fint),
                                                                    str(self.dat[0].tat)))
        for i in range(1, self.totalP):
            completelist[i].serv = completelist[i-1].serv + completelist[i-1].bt 
            completelist[i].wt =  completelist[i].serv - completelist[i].ar 
            if( completelist[i].wt < 0 ) :
                completelist[i].wt = 0
            completelist[i].tat =  completelist[i].bt + completelist[i].wt
            self.tree1.insert("", i, text=str(completelist[i].num), values=(str(completelist[i].wt),
                                                                            str(completelist[i].fint),
                                                                            str(completelist[i].tat)))
        self.ORDERLabel = Label(self.frame3, text="(Note : Processes are in order of execution)",font=("arial", 10), width=30)
        self.ORDERLabel.grid(row=1, column=0, padx=0)

    def PriorPre(self): 
        self.ORDERLabel = Label(self.frame3, text="(Note : Processes are in order of completion)",font=("arial", 10), width=33)
        self.ORDERLabel.grid(row=1, column=0, padx=0)
        self.tree1.heading("service", text="Completion Time",anchor=W)

        # Remaining time = burst time
        for data in self.dat :
            data.rem_bt = data.bt
        complete = 0
        t = 0
        plist = []
        while (complete != self.totalP):
            check = False
            # Find out which process has maximum priority at time t
            for data in self.dat: 
                if ((data.ar <= t) and  # If arrival time less <= T
                    (data.rem_bt > 0) and
                    (data.started == False)) :# remaining time greater than 0 
                    plist.append(data)
                    data.started = True
                    check = True

            if (check == False and not plist): 
                t += 1
                continue

            plist.sort(key=operator.attrgetter('prio'), reverse=True)

            ginput = ganttInput()
            ginput.start = t
            current_process = plist[0]
            current_process.rem_bt -= 1
            t += 1
            ginput.num = current_process.num
            ginput.fin = t

            self.ganttP.append(ginput)
            self.ganttT.append(ginput.fin-ginput.start)
            if (current_process.rem_bt == 0):  
    
                complete += 1
                current_process.fint = t

                current_process.wt = current_process.fint - current_process.ar - current_process.bt

                if (current_process.wt < 0): 
                    current_process.wt = 0
                
                plist.remove(current_process)
        
        self.FINALT = t
        for data in self.dat :
            data.tat = data.wt + data.bt

        self.dat.sort(key=operator.attrgetter('fint'))
        for i in self.tree1.get_children():
            self.tree1.delete(i)

        for i in range(self.totalP) :
            self.tree1.insert("", i, text=str(self.dat[i].num), values=(str(self.dat[i].wt),
                                                                    str(self.dat[i].fint),
                                                                    str(self.dat[i].tat)))

    def RoundRobin(self) :
        self.dat.sort(key=operator.attrgetter('ar'))
        pqueue = queue.Queue(maxsize=11)
        for data in self.dat :
            data.rem_bt = data.bt

        q = int(self.quant.get())
        t = self.dat[0].ar
        pqueue.put(self.dat[0])
        self.dat[0].started = True
        complete = 0
        while( complete != self.totalP) :

            if( pqueue.empty()) :
                t += 1
                for data in self.dat :
                    if( data.ar <= t and data.started == False) :
                        pqueue.put(data)
                        data.started = True
                continue

            current_process = pqueue.get()
            ginput = ganttInput()
            ginput.start = t
            if( current_process.rem_bt > q ) :
                t += q
                current_process.rem_bt -= q
            else :
                t += current_process.rem_bt
                current_process.rem_bt = 0
                current_process.fint = t
                current_process.tat = t - current_process.ar
                current_process.wt = current_process.tat - current_process.bt
                complete += 1
            ginput.fin = t
            ginput.num = current_process.num
            self.ganttP.append(ginput)
            self.ganttT.append(ginput.fin - ginput.start)
            for data in self.dat : 
                if( data != current_process and data.started == False ) :
                    if( data.ar <= t ) :
                        pqueue.put(data)
                        data.started = True
            
            if( current_process.rem_bt != 0 ) :
                pqueue.put(current_process)
        
        self.FINALT = t
        self.dat.sort(key=operator.attrgetter('fint'))
        self.ORDERLabel = Label(self.frame3, text="(Note : Processes are in order of completion)",font=("arial", 10), width=33)
        self.ORDERLabel.grid(row=1, column=0, padx=0)
        self.tree1.heading("service", text="Completion Time",anchor=W)
        
        for i in self.tree1.get_children():
            self.tree1.delete(i)

        for i in range(self.totalP) :
            self.tree1.insert("", i, text=str(self.dat[i].num), values=(str(self.dat[i].wt),
                                                                    str(self.dat[i].fint),
                                                                    str(self.dat[i].tat)))



    def collect_data(self):
        self.FINALT = 0
        self.ganttP.clear()
        self.ganttT.clear()
        self.dat.clear()
        self.totalP = 0
        for row in self.rows:
            data = dataInput()
            i = 0
            available = 1
            for col in row:
                if( i == 0 ) :
                    if( col.get() != "" ) :
                        self.totalP += 1
                    else :
                        available = 0
                        break
                if( i == 0 ) : 
                    data.num = int(col.get())
                elif( i == 1 ) : 
                    data.ar = int(col.get())
                elif( i == 2 ) : 
                    data.bt = int(col.get())
                elif( i == 3 ): 
                    if( col.get() != "" ) :
                        data.prio = int(col.get())
                i += 1
            if( available == 0 ) :
                break
            else:
                self.dat.append(data)

        algoSelected = self.algolist.get()
        if( algoSelected == "FCFS" ) :
            self.FCFS()
        if( algoSelected == "SJF" ) :
            self.SJF()
        if( algoSelected == "SRTF" ) :
            self.SRTF()
        if( algoSelected == "Priority" ) :
            self.Prior()
        if( algoSelected == "Priority(Pre-emption)" ) :
            self.PriorPre()
        if( algoSelected == "Round Robin" ) :
            self.RoundRobin()
        
        avgwt = 0
        for data in self.dat :
            avgwt += data.wt 
        avgwt /= self.totalP
        avgtat = 0
        for data in self.dat :
            avgtat += data.tat 
        avgtat /= self.totalP

        self.AvgWTValue['text'] = str(avgwt)
        self.AvgTATValue['text'] = str(avgtat)

root = Tk()
root.resizable(0, 0) 
my_gui = MyFirstGUI(root)
root.mainloop()