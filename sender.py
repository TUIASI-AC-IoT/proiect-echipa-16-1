import socket
from tkinter import filedialog
from textwrap import wrap
INFO=1
DATA=4
counter=1
continut=[]
asamblare=[]
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
fileName = filedialog.askopenfilename()
file = open(fileName, "r")
file1=file.read()
packetSize = 10
continut=wrap(file1,packetSize)
fileName=fileName[fileName.rfind("/")+1:]
print(f"Ati incarcat fisierul: {fileName}")
file.seek(0, 2);
fileLength = file.tell()
file.seek(0, 0)
nrOfPackets = int(fileLength / packetSize)
nrOfPackets=str(nrOfPackets).zfill(4)
print(f"numarul de octeti:{fileLength}")
print(f"Fisierul necesita : {nrOfPackets} de pachete")
opt=int(input("Ce doriti sa trimiteti catre server:\n"
      "1.Info\n"
      "2.Data\n"))
if(opt==1):
    tosend = str(INFO) + nrOfPackets+fileName;
    tosend1=bytes(tosend.encode())
    print(tosend1)
elif(opt==2):
    for i in range(1, len(continut)+1):
        tosend = str(DATA) +str(counter).zfill(4)+str(nrOfPackets).zfill(4)+str(continut[i-1]);
        counter=counter+1
        s.sendto(tosend.encode('ascii'),("127.0.0.1",5006))
        continut1, (addr,port) = s.recvfrom(1024)
        continut1=continut1.decode('utf-8')
        asamblare.append(continut1)
for i in asamblare:
    print(i)
s.close()