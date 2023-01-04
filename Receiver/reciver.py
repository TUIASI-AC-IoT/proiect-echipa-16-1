import socket
if __name__ == '__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 5006))
    print("witing for connecting")
    while True:
        mesaj, address=s.recvfrom(1024)
        mesaj=bytes(mesaj).decode()

        if(mesaj[0]=="1"):
            print("am primit un fisier de tip info")
            print(mesaj)
            s.sendto("am primit mesajul".encode('utf-8'), address)
        if (mesaj[0] == "4"):
            print("am primit un fisier de tip data")
            print(mesaj)
            s.sendto("am primit mesajul".encode('utf-8'), address)
        if (mesaj[0] == "8"):
            print("am primit un fisier de tip lungime")
            print(mesaj)
            s.sendto("am primit mesajul".encode('utf-8'), address)