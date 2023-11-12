import socket as sck


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # istanzio un socket
    server_address = ("127.0.0.1", 8000)  # tupla con ip e porta (del server - destinatario)

    s.connect(server_address)

    while True:
        operazione = s.recv(4096)
        operazione = operazione.decode()
        if operazione == "EXIT":
            print("ho finito")
            break
        risultato = eval(operazione)
        s.sendall(str(risultato).encode())
    s.close()


if __name__ == "__main__":
    main()
