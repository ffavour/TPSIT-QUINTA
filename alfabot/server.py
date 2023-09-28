import socket as sck
import turtle
import AlphaBot


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    my_address = ("127.0.0.1", 8000)
    s.bind(my_address)
    s.listen()

    bottino = AlphaBot.AlphaBot()
    conn, address = s.accept()

    while True:
        data = conn.recv(4096)
        print(f"ricevuto {data} da {address}")

        dataStr = data.decode()
        comando = dataStr.split(";")

        if comando[0] == "-1":
            print("fine")
            conn.sendall("-1".encode())
            break

        elif not comando[1].isnumeric() or int(comando[1]) <= 0:
            conn.sendall("error".encode())

        else:
            comando[1] = int(comando[1])

            if comando[0] == "f":
                bottino.forward(comando[1])
                conn.sendall("ok".encode())
            elif comando[0] == "b":
                bottino.backward(comando[1])
                conn.sendall("ok".encode())
            elif comando[0] == "l":
                bottino.left(int(comando[1]))
                conn.sendall("ok".encode())

            elif comando[0] == "r":
                bottino.right(int(comando[1]))
                conn.sendall("ok".encode())



            else:
                conn.sendall("error".encode())

    print("uscito")

    conn.close()
    turtle.done()


if __name__ == "__main__":
    main()
