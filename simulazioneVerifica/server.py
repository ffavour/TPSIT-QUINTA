import socket as sck
import threading
import sqlite3

"""Il server riceve costantemente le interrogazioni da tutti i client connessi, tramite protocollo TCP. Ogni client 
può effettuare le seguenti interrogazioni: 
1. chiedere al server se un certo nome file è presente; 
2. chiedere al server il numero di frammenti di un file a partire dal suo nome file; 
3. chiedere al server l’IP dell’host che ospita un frammento a partire nome file e dal numero del frammento; 
4. chiedere al server tutti gli IP degli host sui quali sono salvati i frammenti di un file a partire dal nome file."""


def queryRicercaFile(nomeFile):
    con = sqlite3.connect("file.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT nome FROM files WHERE nome = '{nomeFile}'")
    files = res.fetchall()
    con.close()

    if files:
        return "file è presente nel db"
    else:
        return "file non presente nel db"


def numeroFrammentiPerFile(nomeFile):
    con = sqlite3.connect("file.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT tot_frammenti FROM files WHERE nome = '{nomeFile}'")
    frammenti = res.fetchall()
    con.close()

    if frammenti:
        return frammenti[0][0]
    else:
        return 0


def trovaHostFrammento(nomeFile, nFrammento):
    con = sqlite3.connect("file.db")
    cur = con.cursor()
    res = cur.execute(
        f"SELECT host FROM files fi, frammenti fr WHERE fi.id_file = fr.id_file AND fi.nome = '{nomeFile}' AND fr.n_frammento = {nFrammento}")
    host = res.fetchall()
    con.close()

    if host:
        return host[0][0]
    else:
        return "non presente"


def hostFrammentiFile(nomeFile):
    con = sqlite3.connect("file.db")
    cur = con.cursor()
    res = cur.execute(
        f"SELECT host FROM files fi, frammenti fr WHERE fi.id_file = fr.id_file AND fi.nome = '{nomeFile}'")
    host = res.fetchall()
    con.close()

    if host:
        listaHost = []
        for i in range(len(host)):
            listaHost.append(host[i][0])
        return listaHost
    else:
        return "file non presente in nessun host"


class ClientThread(threading.Thread):
    def __init__(self, conn, address):
        super().__init__()
        self.conn = conn
        self.address = address

    def run(self):
        while True:
            data = self.conn.recv(4096)
            print(f"messaggio ricevuto: {data.decode()} da {self.address}")
            data = data.decode()

            listaDati = data.split(";")
            comando = int(listaDati[0])
            nomeFile = str(listaDati[1])
            nFrammento = int(listaDati[2])

            if comando == 1:
                risposta = queryRicercaFile(nomeFile)
                self.conn.sendall(risposta.encode())
            elif comando == 2:
                nFrammenti = numeroFrammentiPerFile(nomeFile)
                self.conn.sendall(f"ci sono {nFrammenti} frammenti di {nomeFile}".encode())
            elif comando == 3:
                ipHost = trovaHostFrammento(nomeFile, nFrammento)
                self.conn.sendall(f"ip host: {ipHost}".encode())
            elif comando == 4:
                host = hostFrammentiFile(nomeFile)
                self.conn.sendall(f"ip host: {host}".encode())
            else:
                self.conn.sendall(b'error')


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    my_address = ("127.0.0.1", 8000)
    s.bind(my_address)

    s.listen()
    clientList = []

    while True:
        conn, address = s.accept()
        client = ClientThread(conn, address)
        clientList.append(client)
        client.start()


if __name__ == "__main__":
    main()
