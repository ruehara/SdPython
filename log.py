import banco
import os.path
import time
import threading

class Log(object):
    def __init__(self,tempo, id):
        self.tempo = tempo 
        self.id = id
        self.versao = 0

    def escreve_log(self, id, requisicao):
        caminho = ".\\log" + str(self.id) 
        if not os.path.isdir(caminho):
            print("DIRETORIO DE LOG NÃO LOCALIZADO.")
            return -1
        caminhoLog = caminho + "\\log." + str(self.versao) 
        arquivoLog = open(caminhoLog, "a")
        try:
            arquivoLog.write(requisicao + "\n")
            arquivoLog.flush()
        except:
            print("ERRO AO ESCREVER NO LOG")
    
    def recupera(self, id):
        self.bd = banco.Banco() 
        caminho = ".\\log" + str(self.id)
        caminhoSnap = caminho + "\\snap." + str(self.versao)
        if self.versao > 0:
            try:
                snap = open(caminhoSnap, "r")
            except:
                print("ERRO AO ABRIR SNAPSHOT")
                return None
            try:
                for linha in snap:
                    aux = linha.split(' ')        
                    self.bd.create(int(aux[0]),aux[1].strip("\n"))
            except:
                print("ERRO AO RECUPERAR SNAPSHOT")
                return None
        try:
            caminho = ".\\log" + str(self.id)
            caminhoLog = caminho + "\\log." + str(self.versao) 
            arquivoLog = open(caminhoLog,"r")
            if arquivoLog is not None:
                for linha in arquivoLog:
                    aux = linha.split(' ',2)        
                    if int(aux[0]) == 1:
                        self.bd.create(int(aux[1]),aux[2].strip("\n"))
                    elif int(aux[0]) == 3:
                        self.bd.update(int(aux[1]),aux[2].strip("\n"))
                    elif int(aux[0]) == 4:
                        self.bd.delete(int(aux[1]))     
                arquivoLog.close()
        except:
            print("ERRO AO RECUPERAR LOG")
        return self.bd 

    def inicia(self):
        diretorio = "log" + str(self.id) 
        if not os.path.isdir(diretorio):
            try:
                os.mkdir(diretorio)
                caminho = ".\\log" + str(self.id)
                nomeLog = caminho + "\\log.0"
                open(nomeLog,"a")
                return 0
            except OSError:
                print("ERRO AO CRIAR DIRETÓRIO") 
                return -1
        else:
            caminho = ".\\log" + str(self.id)
            arquivos = os.listdir(caminho)
            for i in arquivos:
                if i[:4] == "snap":
                    aux = i.split(".")
                    if int(aux[1]) > self.versao:
                        self.versao = int(aux[1])
            return self.versao

    def escreve_snapshot(self, bnc, versao):
        self.versao = versao
        caminho = ".\\log" + str(self.id)
        nomeSnap = caminho + "\\snap." + str(self.versao)
        nomeLog = caminho + "\\log." + str(self.versao)
        snap = open(nomeSnap, "a")
        open(nomeLog, "a")
        bd = banco.Banco()
        bd = bnc
        for k,v in bd.mapa.items():
            try:
                snap.write(str(k) +" "+ str(v) + "\n")
                snap.flush()
            except:
                print("ERRO")
        if(self.versao > 2):
            try:
                os.remove(caminho + "\\log." + str(self.versao - 3))
            except:
                pass
        if(self.versao > 3):    
            try:
                os.remove(caminho + "\\snap." + str(self.versao - 3))
            except:
                pass