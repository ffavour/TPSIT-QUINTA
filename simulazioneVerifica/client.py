import socket as sck

"""
sintassi: comando;nomefile;frammento     
"""


def menu():
    print("1 - verifica se un file è presente")
    print("2 - chiedi numero di frammenti di un file")
    print("3 - trova host di un frammento")
    print("4 - trova host su cui sono salvati frammenti di n file\n\n")


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # istanzio un socket
    server_address = ("127.0.0.1", 8000)  # tupla con ip e porta (del server - destinatario)

    s.connect(server_address)
    print("connesso")

    while True:
        menu()
        comando = input("inserire un numero: ")
        nomeFile = input("inserire nome file (con estensione): ")
        numeroFrammento = input("inserire numero del frammento: ")

        mex = f"{comando};{nomeFile};{numeroFrammento}"
        if mex == "EXIT":
            break
        s.sendall(mex.encode())
        data = s.recv(4096)
        print(f"messaggio ricevuto: {data.decode()}")

    s.close()


if __name__ == "__main__":
    main()
