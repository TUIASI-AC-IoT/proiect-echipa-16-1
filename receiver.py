import socket
from random import random
import threading
import time

class Reciver:
    def __init__(self, ip, port):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.receptie=[]

    def decodeData(self,packet):
        pID = packet[1:5]
        len = packet[5:9]
        continut = packet[9:]
        return pID, len, continut

    def decodarePachet(self,packet):
        packets = packet[1:5]
        fname = packet[5:]
        return packets, fname

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.UDP_IP, self.UDP_PORT))
        print("witing for connecting")
        pachet_asteptat = 1
        counter = 0;
        while True:

            #for i in range(1, 56):
            packet, address = self.s.recvfrom(1024)
            packet = bytes(packet).decode()
            if (packet[0] == "1"):
                print("am primit un fisier de tip info:")
                nrpachete, numefisier = self.decodarePachet(packet)
                print(f"numarul de pachete:{nrpachete}")
                print(f"numele fisierului:{numefisier}")
                self.s.sendto("am primit mesajul".encode('utf-8'), address)
            if (packet[0] == "4"):
                print("\nam primit un fisier de tip data")
                id, lungime, continut = self.decodeData(packet)
                id = int(id)
                print(f"pachet_asteptat {pachet_asteptat} = {id} id???")
                if id == pachet_asteptat:

                    print(f"s-a receptionat pachetul{id}")
                    print(continut)
                    a = random()

                    if a > 0.3:
                        self.s.sendto(str(continut).encode('ascii'), address)
                        pachet_asteptat = pachet_asteptat + 1
                       # counter+=1
                       # if(counter == 5 ):
                       #      counter = 0
                       # print(f"______COUNTER = {counter}")
                    else:
                        self.s.sendto(str(404).encode('ascii'), address)
                        #------------
                        print(f"DAR ERROR LA RETRIMITERE -> pachet_asteptat_{pachet_asteptat}  -=   counter_{counter}")
                        #-----------






UDP_IP = "127.0.0.1"
UDP_PORT = 5005
reciver = Reciver(UDP_IP, UDP_PORT)
reciver.start()