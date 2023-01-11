import socket
import time
from random import random
import tkinter as tk
import threading
class Reciver:
    def __init__(self):
        self.UDP_IP = ""
        self.UDP_PORT = ""
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
    def validateLogin(self):
        self.UDP_IP=self.ip.get()
        self.UDP_PORT=self.port.get()
        self.var=1

    def interface(self):

        self.root=tk.Tk()
        self.root.geometry("920x720")
        self.root.title("SERVER")
        self.var=tk.IntVar()
        self.root.iconphoto(True, tk.PhotoImage(file ='virtual-server-icon-7.png') )
        self.root.config(background="#dfede9")

        self.T = tk.Text(self.root, height=32, width=82)
        self.port=tk.StringVar()
        self.ip=tk.StringVar()
        self.IPLabel = tk.Label(self.root, text="IP:").grid(row=1, column=0)
        self.IPEntry = tk.Entry(self.root, textvariable=self.ip).grid(row=1, column=1)
        self.PORTLabel = tk.Label(self.root, text="PORT").grid(row=2, column=0)
        self.PORTEntry = tk.Entry(self.root, textvariable=self.port, show='').grid(row=2, column=1)
        self.CONNECTButton = tk.Button(self.root, text="CONNECT", command=self.validateLogin)
        self.CONNECTButton.grid(row=5, column=1)
        self.T.place(x=200,y=0)


        self.root.mainloop()

    def start(self):
        threading.Thread(target=self.interface).start()
        time.sleep(10)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.UDP_IP, int(self.UDP_PORT)))
        print("witing for connecting")
        self.mesaj=tk.Label(self.root,text="✔Ai setat cu SUCCES iP si Port").place(x=32,y=70)
        pachet_asteptat = 1
        counter = 0;
        while True:
            #self.T.insert(tk.END, "waiting for conecting")
            #for i in range(1, 56):
            packet, address = self.s.recvfrom(1024)
            packet = bytes(packet).decode()
            self.T.insert(tk.END, "\n\t\t_______________________________________________\n\t\tAm primit de la:"+str(address)+"\n")
            if (packet[0] == "1"):
                print("         un fisier de tip info:")
                nrpachete, numefisier = self.decodarePachet(packet)
                print(f"numarul de pachete:{nrpachete}")
                print(f"numele fisierului:{numefisier}")
                self.s.sendto("am primit mesajul".encode('utf-8'), address)
            if (packet[0] == "4"):
                print("\nfisier de tip data")
                id, lungime, continut = self.decodeData(packet)
                id = int(id)
                self.T.insert(tk.END, "\t\t      un fisier de tip data\n")
                aux = pachet_asteptat - 1
                old_pac = pachet_asteptat
                if( id == aux):
                    pachet_asteptat -=1

                if(old_pac != pachet_asteptat):
                    self.T.insert(tk.END, "\n\t\t✘TRANSMITEREA anterioara nu a intrat in timp✘\n\t\tPachet asteptat: " + str(pachet_asteptat) + " din nou..\n")
                else:
                    self.T.insert(tk.END, "\t\tPachet asteptat: " + str(pachet_asteptat) + "\n")

                print(f"pachet_asteptat {pachet_asteptat} = {id} id???")
                if id == pachet_asteptat:
                    self.T.insert(tk.END,"\t\tS-a receptionat pachetul: "+str(id)+" cu continutul:"+str(continut)+"\n")
                    print(f"s-a receptionat pachetul{id}")
                    print(continut)
                    a = random()

                    if a > 0.03:
                        self.s.sendto(str(continut).encode('ascii'), address)
                        pachet_asteptat = pachet_asteptat + 1

                    else:
                        self.s.sendto(str(404).encode('ascii'), address)
                        #------------
                        self.T.insert(tk.END,"\t\t_______________________________________________\n\t\t✘ !EROARE LA RETRIMITEREA pachetului " + str(id) + "! ✘\n\t\t_______________________________________________\n\n")
                        print(f"EROARE LA RETRIMITERE ")
                        #-----------
    def proces(self):
        threading.Thread(target=self.start).start()
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
reciver = Reciver()
reciver.proces()