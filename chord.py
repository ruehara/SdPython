import server
import os
import config
import time
import threading

class Chord:
    def __init__(self):
        self.qnt_key = None
        self.qnt_nodes = None
        self.cfg = config.Config()
        self.host = self.cfg.getHost().strip("\n")
        self.portaInicial = int(self.cfg.getMinPort().strip("\n"))
        self.srv = [] #lista de servidores
        self.id = []
        self.portas = []
        self.qnt_key = None
        self.qnt_nodes = None

    def main(self):
        self.qnt_key = input("Quantidade de Bits: ")
        self.qnt_nodes = input("Quantidade de Nós: ")
        self.snap_time = input("Tempo Snapshot (seg): ")

        self.id.insert(0, 2**int(self.qnt_key) - 1)
        self.portas.insert(0, self.portaInicial)

        for i in range(1, int(self.qnt_nodes)):
            self.id.insert(i, int(self.id[i-1] - ((2**int(self.qnt_key))/int(self.qnt_nodes))))
            self.portas.insert(i, self.portaInicial+ 4*i)

        for i in range(0, int(self.qnt_nodes)):
            if i == 0:
                self.srv.insert(i, (self.id[int(self.qnt_nodes)-1], self.id[i], self.id[i+1],self.portas[int(self.qnt_nodes)-1], self.portas[i], self.portas[i+1]))
            elif i == (int(self.qnt_nodes )-1):
                self.srv.insert(i, (self.id[i-1], self.id[i], self.id[0],self.portas[i-1], self.portas[i], self.portas[0]))
            else:
                self.srv.insert(i, (self.id[i-1], self.id[i], self.id[i+1],self.portas[i-1], self.portas[i], self.portas[i+1]))

        chord = open("thisChord.txt","w")
        for i in range(0, int(self.qnt_nodes) ): #inicia os servidores passando os parametros criados pelo chord
            cAnt, cAtu, cSuc, pAnt, pAtu, pSuc = self.srv[i]
            chord.write(self.qnt_key + " " + self.qnt_nodes + " " + str(cAnt) + " " + str(cAtu) + " " + str(cSuc) + " " + str(pAnt) + " " + str(pAtu) + " " + str(pSuc) +  " " + self.snap_time + "\n")
            os.system("start /B start cmd.exe @cmd /k python server.py " + self.qnt_key + " " + self.qnt_nodes + " " + str(cAnt) + " " + str(cAtu) + " " + str(cSuc) + " " + str(pAnt) + " " + str(pAtu) + " " + str(pSuc) +  " " + self.snap_time)

        #inicia cliente
        os.system("start /B start cmd.exe @cmd /k python client.py ")

if __name__ == '__main__':
    chord = Chord()
    chord.main()