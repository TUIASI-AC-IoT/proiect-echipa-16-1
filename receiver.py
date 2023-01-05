import socket
receptie=[]
def decodeData(packet):
    pID = packet[1:5]
    len = packet[5:9]
    continut=packet[9:]
    return pID, len, continut

def decodarePachet(packet):
    packets = packet[1:5]
    fname = packet[5:]
    return packets, fname

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 5006))
print("witing for connecting")
packet_asteptat=1
while True:
    for i in range(1,56):
        packet, address=s.recvfrom(1024)
        packet=bytes(packet).decode()
        if(packet[0]=="1"):
            print("am primit un fisier de tip info:")
            nrpachete,numefisier=decodarePachet(packet)
            print(f"numarul de pachete:{nrpachete}")
            print(f"numele fisierului:{numefisier}")
            s.sendto("am primit mesajul".encode('utf-8'), address)
        if (packet[0] == "4"):
            print("am primit un fisier de tip data")
            id,lungime,continut =decodeData(packet)
            id = int(id)
            print(id)
            if id==packet_asteptat:
                print(f"s-a receptionat pachetul{id}")
                print(continut)
                s.sendto(str(continut).encode('ascii'), address)
        packet_asteptat=packet_asteptat+1