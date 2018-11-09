from concurrent import futures
import grpc
import servicos_pb2
import servicos_pb2_grpc
import threading 
import fila
import banco
import time
import os
import random
import sys
import config
from colorama import init
init()

TIMEOUT = 60 * 60 * 24

class Server(servicos_pb2_grpc.RequisicaoServicer):
    def __init__(self, bits, srv, cAnt, cAtu, cSuc, pAnt, pAtu, pSuc, tsnap):
        self.port = pAtu
        self.bits = bits
        self.srv = srv
        self.cAnt = cAnt
        self.cAtu = cAtu
        self.cSuc = cSuc
        self.pAnt = pAnt
        self.pAtu = pAtu
        self.pSuc = pSuc
        self.time_snap = tsnap
        self.chaves = []
        self.f1 = fila.Fila()
        self.f2 = fila.Fila()
        self.f3 = fila.Fila()
        self.f4 = fila.Fila()
        self.fresp = fila.Fila()
        self.bd = banco.Banco()
        self.cfg = config.Config()
        self.host = self.cfg.getHost().strip("\n")
        self.visitado = False

    def Conectado(self, request, context):
        print(request.chave + " conectado")
        return servicos_pb2.Resultado(resposta="Conectado ao Servidor: "+str(self.cAtu))

    def Create(self,request,context):
        requisicao = "1 " + request.chave + " " + request.valor
        msg = self.trata_resp(requisicao)
        print("procurando...")
        return servicos_pb2.Resultado(resposta=msg)

    def Read(self, request, context):
        requisicao = "2 " + request.chave
        msg = self.trata_resp(requisicao)
        print("procurando...")
        return servicos_pb2.Resultado(resposta=msg)

    def Update(self, request, context):
        requisicao = "3 " + request.chave + " " + request.valor
        msg = self.trata_resp(requisicao)
        print("procurando...")
        return servicos_pb2.Resultado(resposta=msg)

    def Delete(self, request, context):
        requisicao = "4 " + request.chave
        msg = self.trata_resp(requisicao)
        print("procurando...")
        return servicos_pb2.Resultado(resposta=msg)
 
    def main(self):
        self.imprime_infos()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        servicos_pb2_grpc.add_RequisicaoServicer_to_server(self, server)
        server.add_insecure_port(self.host+':'+str(self.pAtu))
        server.start()
        self.channel = grpc.insecure_channel(self.host+":"+str(self.pAnt))
        self.stubAnt = servicos_pb2_grpc.RequisicaoStub(self.channel)
        self.channel = grpc.insecure_channel(self.host+":"+str(self.pSuc))
        self.stubSuc = servicos_pb2_grpc.RequisicaoStub(self.channel)
        try:
            while True:
                time.sleep(TIMEOUT)
        except KeyboardInterrupt:
            pass
            server.stop(5)

    def imprime_infos(self):
        print('\033[37m'+"\tAnte.\tServ.\tSuce. \nId:\t" + str(self.cAnt)+"\t"+'\033[32m' + str(self.cAtu)+"\t"+'\033[37m'+str(self.cSuc))
        print("Porta:\t"+ str(self.pAnt)+"\t"+'\033[32m' +str(self.pAtu)+"\t"+'\033[37m'+str(self.pSuc)+"\n")
        if self.cAnt < self.cAtu:
            for i in range(0, self.cAnt):
                if i==0:
                    self.chaves.insert(i,self.cAtu)
                self.chaves.insert(i,i)
        else:
            for i in range(self.cAtu, self.cAnt, 1):
                j = 0
                self.chaves.insert(j,i)
                j = j + j
        print("Chaves: " + str(self.chaves))

    def trata_resp(self, requisicao):
        if not self.visitado:
            self.visitado = True
            cm = str(requisicao)
            cm = cm.split(' ',2)
            key = int(cm[1])
            if key in self.chaves:
                print("encontrou..")
                self.f1.insere(requisicao)
                while self.fresp.vazia():
                    pass
                msg = self.fresp.retira()
                #msg = str(self.cAtu)
                self.visitado = False
            else:
                retorno = self.retransmite(requisicao)
                self.visitado = False
                msg = retorno.resposta
        else:
            msg = "Chave não existe!"
            self.visitado = False
        return msg

    def retorna_banco(self, id):
        pass

    def retransmite(self, requisicao):
        #req = self.f4.retira()
        cm = str(requisicao)
        cm = cm.split(' ',2)
        key = int(cm[1])
        if key >= self.cAnt:
            if cm[0] == '1':
                retorno = self.stubAnt.Create(servicos_pb2.CreateUpdate(chave=cm[1], valor=cm[2]))
            elif cm[0] == '2':
                retorno = self.stubAnt.Read(servicos_pb2.ReadDelete(chave=cm[1]))
            elif cm[0] == '3':
                retorno = self.stubAnt.Update(servicos_pb2.CreateUpdate(chave=cm[1], valor=cm[2]))
            elif cm[0] == '4':
                retorno = self.stubAnt.Delete(servicos_pb2.ReadDelete(chave=cm[1]))
        else:
            if cm[0] == '1':
                retorno = self.stubSuc.Create(servicos_pb2.CreateUpdate(chave=cm[1], valor=cm[2]))
            elif cm[0] == '2':
                retorno = self.stubSuc.Read(servicos_pb2.ReadDelete(chave=cm[1]))
            elif cm[0] == '3':
                retorno = self.stubSuc.Update(servicos_pb2.CreateUpdate(chave=cm[1], valor=cm[2]))
            elif cm[0] == '4':
                retorno = self.stubSuc.Delete(servicos_pb2.ReadDelete(chave=cm[1]))
        return retorno

    def duplica_thread(self):
        while True:
            while not self.f1.vazia():
                try:
                    comando = self.f1.retira()
                    self.f2.insere(comando)
                    self.f3.insere(comando)
                except:
                    pass

    def log_thread(self):
        while True:
            while not self.f2.vazia():
                try:
                    requisicao = str(self.f2.retira())
                    cm = requisicao.split(' ',2)
                    if int(cm[0]) != 2:
                        #salva_log()
                        pass
                except:
                    pass

    def banco_thread(self):
        while True:
            while not self.f3.vazia():
                try:
                    cm = self.f3.retira()
                    cm = str(cm)
                    cm = cm.split(' ',2)
                    ok = False
                    if cm[0] == '1' :
                        if self.bd.create(int(cm[1]),cm[2]):
                            ok = True
                            msg = "OK"
                    elif cm[0] == '2' :
                            read = self.bd.read(int(cm[1]))
                            if read:
                                msg = "Chave:" + str(cm[1]) +" Valor: " + read
                                ok = True
                    elif cm[0] == '3' :
                        if self.bd.update(int(cm[1]),cm[2]):
                            msg = "OK"
                            ok = True
                    elif cm[0] == '4' :
                        if self.bd.delete(int(cm[1])):
                            msg = "OK"
                            ok = True
                    if not ok:
                        msg = "NOK"
                    self.fresp.insere(msg)
                except:
                    pass

    def run(self):
        duplica = threading.Thread(target=self.duplica_thread, name="duplica",args=())
        duplica.setDaemon(True)
        duplica.start()

        log = threading.Thread(target=self.log_thread, name="log",args=())
        log.setDaemon(True)
        log.start()

        banco = threading.Thread(target=self.banco_thread, name="banco",args=())
        banco.setDaemon(True)                
        banco.start()

        self.main()

def run_server():
    bits = int(sys.argv[1])
    srv = int(sys.argv[2])
    cAnt = int(sys.argv[3])
    cAtu = int(sys.argv[4])
    cSuc = int(sys.argv[5])
    pAnt = int(sys.argv[6])
    pAtu = int(sys.argv[7])
    pSuc = int(sys.argv[8])
    tsnap = int(sys.argv[9])

    server = Server(bits, srv, cAnt, cAtu, cSuc, pAnt, pAtu, pSuc, tsnap)
    server.run()

if __name__ == '__main__':
    run_server()