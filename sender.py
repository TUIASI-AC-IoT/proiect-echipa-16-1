import socket
import threading

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
    def decodeACK(self,packet):
        pID=packet[0:1]
        continut=packet[1:]
        return pID,continut

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
            while self.pachetID<len(self.continut):
                for i in range(self.windowSize):
                    tosend = str(self.DATA) + str(counter).zfill(4) + str(nrOfPackets).zfill(4) + str(self.continut[i]);
                    self.s.sendto(tosend.encode('ascii'), ("127.0.0.1", 5005))
                    continut1, (addr, port) = self.s.recvfrom(1024)
                    continut1 = continut1.decode('utf-8')
                    dsa,continut1=self.decodeACK(continut1)
                    print(counter)
                    print(dsa)
                    while dsa!=counter:
                        print(counter)
                        tosend = str(self.DATA) + str(counter).zfill(4) + str(nrOfPackets).zfill(4) + str(self.continut[i]);
                        self.s.sendto(tosend.encode('ascii'), ("127.0.0.1", 5005))
                        continut1, (addr, port) = self.s.recvfrom(1024)
                        continut1 = continut1.decode('utf-8')
                        dsa, continut1 = self.decodeACK(continut1)

                    self.asamblare.append(continut1)
                    self.pachetID = self.pachetID + 1
                    counter=counter+1
                del self.continut[0:5]
                self.pachetID -= self.windowSize
        for i in self.asamblare:
            print(i)
        self.s.close()
    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread(target=self.proces).start()

sender=Sender()
sender.start()
