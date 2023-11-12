import socket as sck
import threading
import sqlite3

"""Sviluppare un client TCP che sia in grado di ricevere un’operazione matematica (ad es. 5+6*(454483+3447)) sotto 
forma di stringa e che la esegua utilizzando la funzione eval nativa di Python. Il risultato verrà riconvertito in 
stringa ed inviato al server. Nel caso in cui il client riceva la stringa “exit”, esso dovrà terminare. 
Sviluppare un server che inizialmente legga il database e si carichi le informazioni all’interno di una opportuna struttura dati 
accessibile ai thread di ogni connessione. 
Successivamente il server inizia ad accettare connessioni dai client e a 
eseguire i relativi thread: utilizzare un contatore incrementale (1,2,3,…) per identificare i thread, che tornerà 
utile all’interno del singolo thread per inviare le operazioni ai client corrispondenti, secondo la colonna “client”. 
Ciascun thread dovrà inviare al suo client l’operazione da eseguire e dovrà ricevere il risultato, stampandolo a 
video con la print seguente: 
print (f"{operazione} = {risultato} from {client_ip} - {client_port}") Sul server non 
devono essere presenti altre stampe a video, quindi rimuovere le print di debug prima della consegna, Al termine 
delle operazioni il thread invierà al client la stringa “exit” ed il client terminerà la sua esecuzione.

Esempio con riga 4 della tabella: il client 1 dovrà eseguire l’operazione matematica “56*43”, quindi il thread 1 
invierà al suo client l’operazione “56*43” edne riceverà il risultato."""


def leggiOperazioniDB(idClient):
    con = sqlite3.connect("operations.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT operation FROM operations WHERE client = '{idClient}'")
    operazioni = res.fetchall()
    con.close()

    if operazioni:
        listaOperazioni = []
        for i in range(len(operazioni)):
            listaOperazioni.append(operazioni[i][0])
        return listaOperazioni
    else:
        return "nessuna operazione disponibile"


class ClientThread(threading.Thread):
    def __init__(self, conn, address, idC):
        super().__init__()
        self.conn = conn
        self.address = address
        self.idC = idC

    def run(self):
        listaOperazioni = leggiOperazioniDB(self.idC)
        listaOperazioni.append("EXIT")
        listaRisultati = []

        for elemento in listaOperazioni:
            self.conn.sendall(elemento.encode())
            risultato = self.conn.recv(4096)
            risultato = risultato.decode()
            print(f"{elemento} = {risultato} from {self.address[0]} - {self.address[1]}")
            listaRisultati.append(risultato)


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    my_address = ("127.0.0.1", 8000)
    s.bind(my_address)

    s.listen()
    clientList = []
    idClient = 1

    while True:
        conn, address = s.accept()
        client = ClientThread(conn, address, idClient)
        clientList.append(client)
        client.start()

        idClient += 1


if __name__ == "__main__":
    main()
