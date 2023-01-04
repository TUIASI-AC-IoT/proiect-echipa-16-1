import socket
from tkinter import filedialog
INFO=1
DATA=4
LUNGIME=8
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
fileName = filedialog.askopenfilename()
file = open(fileName, "r")
print(f"Ati incarcat fisierul: {fileName}")
file.seek(0, 2);
fileLength = file.tell()
file.seek(0, 0)
sizeOfFrame = 100
nrOfPackets = int(fileLength / sizeOfFrame)

print(f"Fisierul necesita : {nrOfPackets} de pachete")
opt=int(input("Ce doriti sa trimiteti catre server:\n "
      "1.Info\n"
      "2.Data\n"
      "3.Dimensiunea\n"))
if(opt==1):
    tosend = str(INFO) + str(nrOfPackets);
elif(opt==2):
    tosend = str(DATA) + str(file.read());
elif(opt==3):
    tosend=str(LUNGIME)+fileName;
else:
    print("ASD")
s.sendto(tosend.encode('utf-8'),("127.0.0.1",5006))
print(s.recvfrom(1024))