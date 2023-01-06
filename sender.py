import socket
import threading
import datetime
import time
from tkinter import filedialog
from textwrap import wrap

class Sender:
    def __init__(self):
        self.INFO = 1
        self.DATA = 4
        self.counter = 1
        self.continut = []
        self.asamblare = []
        self.pachetID=0
        self.windowSize=5
    def proces(self):
        fileName = filedialog.askopenfilename()
        file = open(fileName, "r+")
        file1 = file.read()

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

        timp_introdus = 0.062
        print(f"numarul de octeti:{fileLength}")
        print(f"Fisierul necesita : {nrOfPackets} de pachete")
        opt = int(input("Ce doriti sa trimiteti catre server:\n"
                        "1.Info\n"
                        "2.Data\n"))
        if (opt == 1):
            tosend = str(self.INFO) + nrOfPackets + fileName;
            tosend1 = bytes(tosend.encode())
            print(tosend1)

        elif (opt == 2):
            print(f" len(self.continut) = {len(self.continut)}")
            while self.pachetID <len(self.continut):
               #for i in range(self.windowSize):
                i = 0
                while(i < self.windowSize):

                    tosend = str(self.DATA) + str(counter).zfill(4) + str(nrOfPackets).zfill(4) + str(self.continut[i]);

                    start = datetime.datetime.now()

                    self.s.sendto(tosend.encode('ascii'), ("127.0.0.1", 5005))

                    time.sleep(0.05)

                    continut1, (addr, port) = self.s.recvfrom(1024)

                    stop = datetime.datetime.now()
                    delta_timp = stop - start

                    print(f"*****{(delta_timp.total_seconds()  )}*****")

                    continut1 = continut1.decode('utf-8')


                    delta = float(delta_timp.total_seconds())
                    print(f"DELTA = {delta}   >   timp_introdus{timp_introdus} ? ")
                    if(timp_introdus < delta):
                       ok = 1
                    else:
                       ok = 0
                    print(f"ok = {ok}")
                    if ((continut1 == "404") or (ok == 1)):

                        print(f"----\ncontinut =  {continut1} || id = {self.pachetID}  || counter = {counter} || i = {i}\n")
                    else:
                        print(f"continut =  {continut1} || id = {self.pachetID}  || counter = {counter} || i = {i}")
                        self.asamblare.append(continut1)
                        self.pachetID = self.pachetID + 1
                        counter = counter + 1
                        i = i + 1;
                del self.continut[0:5]
                self.pachetID -= self.windowSize



        for i in self.asamblare:
            print(i)
        for i in self.asamblare:
            print(i, end = " ")

        self.s.close()
    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread(target=self.proces).start()

sender=Sender()
sender.start()
