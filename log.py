import banco
import os.path
import time
import threading

class Log(object):
    def __init__(self,tempo, id):
        self.U = tempo #tempo para criar novo arquivo de log
        self.id = id

    def escreve(self, id, requisicao):
        caminho = ".\log" + str(self.id) #diretorio dos arquivos de log
        #encontrar o ultimo arquivo de log
        if not os.path.isdir(caminho):
            print("Diretorio de Log nao localizado.")
            return -1
        arquivos = os.listdir(caminho)
        maior = 0
        for i in arquivos:
            if i[:3] == "log":
                x = i.split(".")
                if int(x[1]) > int(maior):
                    maior = x[1]
        #print(maior)
        #print(requisicao)
        caminhoLog = caminho + "\log." + maior #log no qual deve ser escrito
        arquivoLog = open(caminhoLog, "a") #referencia para arquivo
        #print(arquivoLog.name)
        try:
            cm = requisicao.split(' ',2)
            if int(cm[0]) != 2 : # se for diferente de Read 
                arquivoLog.write(requisicao + "\n")
                arquivoLog.flush()
        except:
            print("ERRO AO ESCREVER NO LOG")
    
    def recupera(self, id):
        try:
            self.bd = banco.Banco() #instância do banco para retorno
        except:
            print("Erro ao instanciar banco")
            return None
            
        caminho = ".\log" + str(self.id) #diretorio dos arquivos de log
        #localizar o maior snapshot
        
        if not os.path.isdir(caminho):
            print("Log não localizado")
            return -1
        
        arquivos = os.listdir(caminho)
        
        maior = 0
        for i in arquivos:
            if i[:4] == "snap":
                x = i.split(".")
                if int(x[1]) > int(maior):
                    maior = x[1]
        
        print(maior)
        caminhoSnap = caminho + "\snap." + maior #snapshot que deve ser retornado
        print(caminhoSnap)
        
        try:
            snap = open(caminhoSnap, "r") #referencia para arquivo
        except:
            print("Erro ao abrir snapshot")
            return None

        #gravando o snapshot no banco de dados
        try:
            for linha in snap:
                aux = linha.split(' ')        
                self.bd.create(int(aux[0]),aux[1].strip("\n"))
        except:
            print("Erro ao recuperar snapshot")
            return None

        #recuperando último log depois do último snapshot
        try:
            caminhoLog = caminho + "\log." + maior #log que deve ser executado
            arquivoLog = open(caminhoLog,"r")

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
            print("Erro ao recuperar log")
            return None
        
        return self.bd #retorna banco

    def inicia(self):
        diretorio = "log" + str(self.id) #nomeia diretorio
        if not os.path.isdir(diretorio): #testa se diretorio já existe
            try:
                os.mkdir(diretorio) #cria diretorio
            except OSError:
                print("Erro ao criar diretório de LOG") 
                return -1
        
        bd = banco.Banco()
        
        #cria arquivos de log e snapshots
        x = 0 #contador do número do log e snapshot
        caminho = ".\log" + str(self.id) #caminho para gravacao do log e snapshot
        nomeLog = caminho + "\log.0" #nome do primeiro arquivo de log
        open(nomeLog,"a") #abre primeiro arquivo de log (log.0)
        while True:
            x = x + 1 #incrementa contador
            nomeLog = caminho + "\log." + str(x) #atualiza nome do log
            nomeSnapshot = caminho + "\snap." + str(x) #atualiza nome do snapshot
            time.sleep(self.U) #tempo até criar proximo log e snapshot
            snap = open(nomeSnapshot, "a") #cria arquivo de snapshot
            #FAZER: copia estado atual do banco para snapshot
            arquivo = open(nomeLog,"a") #cria arquivo de log
            
            #apaga log e snapshot antigos
            if(x > 2):
                try:
                    os.remove(caminho + "\log." + str(x-3))
                except:
                    pass
            if(x > 3):    
                try:
                    os.remove(caminho + "\snap." + str(x-3))
                except:
                    pass

    def start(self):
        snap = threading.Thread(target=self.inicia, name="snap",args=())
        snap.setDaemon(True)
        snap.start()

#variavel =  Log(5)
#variavel.inicia(984798274)
#x = banco.Banco()
#print(x)
#x = variavel.recupera(9)
#print(x)
#variavel.escreve(9, "1 200 chave200")

#print(x.read(1999))


#cria = threading.Thread(target=self.criaArquivosLog, args=(id,))
#cria.setDaemon(True)
#cria.start()