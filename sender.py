import socket
import threading
import datetime
from tkinter import *
import time
from tkinter import filedialog
import tkinter as tk
from textwrap import wrap

class Sender:
    def __init__(self):
        self.INFO = 1
        self.DATA = 4
        self.counter = 1
        self.continut = []
        self.asamblare = []
        self.pachetID=0
        self.var=0
        threading.Thread(target=self.interface).start()
        self.running=1

    def interface(self):

        self.root = tk.Tk()
        self.root.geometry("920x720")
        self.root.title("CLIENT  (go back n)")

        #self.root.iconphoto(True, tk.PhotoImage(file='cliente.png'))
        self.root.config(background="#dfede9")

        self.T = tk.Text(self.root, height=22, width=82)
        self.ansLabel=tk.Label(self.root,text="Fisierul reasamblat:").place(x=200,y=390)
        self.Tans = tk.Text(self.root, height=16, width=82)
        self.timer = tk.StringVar()
        self.n = tk.StringVar()
        self.opt = tk.StringVar()
        self.T.place(x=200, y=0)
        self.Tans.place(x=200,y=420)
        self.a = tk.Button(self.root, text="Incarcati fisier", command=self.get_fisier).place(x=49, y=23)
        self.nLabel = tk.Label(self.root, text="   Dimensiunea ferestrei:").place(x=0, y = 100)
        self.nEntry = tk.Entry(self.root, textvariable=self.n).place(x=9, y = 120)
        self.timerLabel = tk.Label(self.root, text="Timp transfer(s):").place(x=9, y = 180)
        self.timerEntry = tk.Entry(self.root, textvariable=self.timer, show='').place(x=9, y = 200)

        self.optLabel = tk.Label(self.root, text="  1 = Info | 2 = Data").place(x=9, y=240)
        self.optEntry = tk.Entry(self.root, textvariable=self.opt, show='').place(x=9, y=260)
        self.Trimite=tk.Button(self.root,text="Timite",command=self.startproces).place(x=9,y=290)

        self.root.mainloop()

    def startproces(self):
        self.var=1
    def get_fisier(self):
        self.fileName=filedialog.askopenfilename()
        self.T.insert(tk.END, "Ati introdus fisierul: " + str(self.fileName) + "\n")

    def proces(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        global z
        fileName = self.fileName
        file = open(fileName, "r+")
        file1 = file.read()
        self.windowSize = self.n.get()
        self.timer = self.timer.get()
        packetSize = 10
        self.windowSize=int(self.windowSize)
        self.continut = wrap(file1, packetSize)
        fileName = fileName[fileName.rfind("/") + 1:]
        print(f"Ati incarcat fisierul: {fileName}")
        file.seek(0, 2);
        fileLength = file.tell()
        file.seek(0, 0)
        nrOfPackets = int(fileLength / packetSize)
        nrOfPackets = str(nrOfPackets).zfill(4)
        counter = 1
        self.T.insert(tk.END, "Fisierul are dimensiunea de :"+str(fileLength)+" octeti\n")
        self.T.insert(tk.END, "Fisierul este impartit in: " + str(nrOfPackets) + " de pachete\n")
        timp_introdus = self.timer
        print(f"numarul de octeti:{fileLength}")
        print(f"Fisierul necesita : {nrOfPackets} de pachete")
        opt = int(self.opt.get())
        if (opt == 1):
            tosend = str(self.INFO) + nrOfPackets + fileName;
            tosend1 = bytes(tosend.encode())
            print(tosend1)
            self.s.sendto(tosend.encode('ascii'), ("127.0.0.3", 5005))

        elif (opt == 2):
            print(f" len(self.continut) = {len(self.continut)}")
            i=1
            frames=int(nrOfPackets)
            while i <=frames:
                z = 0
                k=i
                while k<i+self.windowSize and k<=frames:
                    tosend = str(self.DATA) + str(k).zfill(4) + str(len(self.continut)).zfill(4)
                    start = datetime.datetime.now()
                    self.s.sendto(tosend.encode('ascii'), ("127.0.0.3", 5005))
                    address = 5005
                    self.T.insert(tk.END, "\n\nAm trimis catre SERVER pachetul:" + str(k) + "\n")
                    time.sleep(0.05)
                    k=k+1
                k1=i
                while k1<i+self.windowSize and k1<=frames:
                    continut1, (addr, port) = self.s.recvfrom(1024)
                    stop = datetime.datetime.now()
                    delta_timp = stop - start
                    print(f"***{(delta_timp.total_seconds()  )}***")
                    continut1 = continut1.decode('utf-8')
                    delta = float(delta_timp.total_seconds())
                    print(f"DELTA = {delta}   >   timp_introdus{timp_introdus} ? ")
                    if(float(timp_introdus) < delta):
                       ok = 1
                    else:
                       ok = 0
                    print(f"ok = {ok}")
                    if ((continut1 == "404") or (ok == 1)):
                        self.T.insert(tk.END, "\n_________________________________________________________________________________")
                        if(continut1 == "404"):
                            self.T.insert(tk.END,"\n✘ !EROARE PACHETUL  " + str(k1) + " NU A PUTUT AJUNGE! ✘")
                        if(ok == 1):
                            self.T.insert(tk.END,"\n✘ Intarziere pachet "+str(k1) + ": (Timp de transfer__" + str(delta) + "  <  " + str(timp_introdus) + "__Timp introdus) ✘")
                        self.T.insert(tk.END, "\n_________________________________________________________________________________")
                        print(f"----\ncontinut =  {continut1} || id = {self.pachetID}  || counter = {counter} || i = {i}\n")
                        break
                    else:
                        self.T.insert(tk.END, "Pachetul: " + str(k1) + " a ajuns cu succes  ✔\n")
                        print(f"continut =  {continut1} || id = {self.pachetID}  || counter = {counter} || i = {i}")
                        self.asamblare.append(continut1)
                        del (self.continut[0:9])
                        z=z+1
                    k1=k1+1
                i=i+z
        for i in self.asamblare:
            print(i)
        for i in self.asamblare:
            print(i, end = " ")
            self.Tans.insert(tk.END, str(i)+" ")

        self.s.close()
    def start(self):

        threading.Thread(target=self.proces).start()

sender=Sender()
while int(sender.var)==0:
    time.sleep(1)
else:
    sender.start()
