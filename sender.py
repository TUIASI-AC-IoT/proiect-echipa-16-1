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

    def proces(self):
        fileName = self.fileName
        file = open(fileName, "r+")
        file1 = file.read()
        self.windowSize = self.n.get()
        self.timer = self.timer.get()

        packetSize = 10

        self.continut = wrap(file1, packetSize)

        fileName = fileName[fileName.rfind("/") + 1:]
        print(f"Ati incarcat fisierul: {fileName}")
        file.seek(0, 2);
        fileLength = file.tell()
        file.seek(0, 0)
        nrOfPackets = int(fileLength / packetSize)
        nrOfPackets = str(nrOfPackets).zfill(4)
        counter = 1

        timp_introdus = self.timer
        print(f"numarul de octeti:{fileLength}")
        print(f"Fisierul necesita : {nrOfPackets} de pachete")
        opt = int(self.opt.get())
        if (opt == 1):
            tosend = str(self.INFO) + nrOfPackets + fileName;
            tosend1 = bytes(tosend.encode())
            print(tosend1)
            self.s.sendto(tosend.encode('ascii'), ("127.0.0.1", 5005))
        elif (opt == 2):
            print(f" len(self.continut) = {len(self.continut)}")
            while self.pachetID <len(self.continut):
               #for i in range(self.windowSize):
                i = 0
                while(i < int(self.windowSize)):

                    tosend = str(self.DATA) + str(counter).zfill(4) + str(nrOfPackets).zfill(4) + str(self.continut[i]);

                    start = datetime.datetime.now()

                    self.s.sendto(tosend.encode('ascii'), ("127.0.0.1", 5005))
                    address = 5005
                    self.T.insert(tk.END,"\n\nAm trimis catre SERVER pachetul:" + str(counter)+"\n")
                    time.sleep(0.05) #intarziere intentionata pentru a putea calcula timpul de transfer si primire

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
                            self.T.insert(tk.END,"\n✘ !EROARE PACHETUL  " + str(counter) + " NU A PUTUT AJUNGE! ✘")
                        if(ok == 1):
                            self.T.insert(tk.END,"\n✘ Intarziere pachet "+str(counter) + ": (Timp de transfer__" + str(delta) + "  <  " + str(timp_introdus) + "__Timp introdus) ✘")
                        self.T.insert(tk.END, "\n_________________________________________________________________________________")
                        print(f"----\ncontinut =  {continut1} || id = {self.pachetID}  || counter = {counter} || i = {i}\n")
                    else:
                        self.T.insert(tk.END, "Pachetul: " + str(counter) + " a ajuns cu succes  ✔\n")
                        print(f"continut =  {continut1} || id = {self.pachetID}  || counter = {counter} || i = {i}")
                        self.asamblare.append(continut1)
                        self.pachetID = self.pachetID + 1
                        counter = counter + 1
                        i = i + 1;
                        if(i == len(self.continut)):
                            i = 999
                            self.pachetID = 999
                del self.continut[0:int(self.windowSize)]
                self.pachetID -= int(self.windowSize)

        for i in self.asamblare:
            print(i)
        for i in self.asamblare:
            print(i, end = " ")
            self.Tans.insert(tk.END, str(i)+" ")

        self.s.close()
    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread(target=self.proces).start()

sender=Sender()
while int(sender.var)==0:
    time.sleep(1)
else:
    sender.start()
