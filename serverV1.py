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

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Server(servicos_pb2_grpc.RequisicaoServicer):
    def __init__(self, bits, srv, cAnt, cAtu, cSuc, pAnt, pAtu, pSuc):
        self.port = pAtu
        self.bits = bits
        self.srv = srv
        self.cAnt = cAnt
        self.cAtu = cAtu
        self.cSuc = cSuc
        self.pAnt = pAnt
        self.pAtu = pAtu
        self.pSuc = pSuc
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
        print(request.chave)
        return servicos_pb2.Resultado(resposta="Conectado ao Servidor: "+str(self.cAtu))

    def Create(self,request,context):
        requisicao = "1 " + request.chave + " " + request.valor
        msg = self.trata(requisicao)
        print("passou por aqui")
        return servicos_pb2.Resultado(resposta=msg)

    def Read(self, request, context):
        requisicao = "2 " + request.chave
        #msg = f0.insere(requisicao)

    def Update(self, request, context):
        requisicao = "3 " + request.chave + " " + request.valor
        #msg = f0.insere(requisicao)

    def Delete(self, request, context):
        requisicao = "4 " + request.chave
        #msg = f0.insere(requisicao)
   
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
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            pass
            server.stop(0)

    def imprime_infos(self):
        print("\tAnte.\tServ.\tSuce. \nId:\t" + str(self.cAnt)+"\t"+str(self.cAtu)+"\t"+str(self.cSuc))
        print("Port:\t"+ str(self.pAnt)+"\t"+str(self.pAtu)+"\t"+str(self.pSuc)+"\n")
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

    def trata(self, requisicao):
        if not self.visitado:
            self.visitado = True
            cm = str(requisicao)
            cm = cm.split(' ',2)
            key = int(cm[1])
            if key in self.chaves:
                #self.f1.insere(requisicao)
                msg = str(self.cAtu)
                self.visitado = False
            else:
                retorno = self.retransmite(requisicao)
                self.visitado = False
                msg = retorno.resposta
        else:
            msg = "Chave não existe!"
            self.visitado = False
        return msg

    def retransmite(self, requisicao):
        #req = self.f4.retira()
        cm = str(requisicao)
        cm = cm.split(' ',2)
        key = int(cm[1])
        if key > self.cAnt:
            retorno = self.stubAnt.Create(servicos_pb2.CreateUpdate(chave=cm[1], valor=cm[2]))
        else:
            retorno = self.stubSuc.Create(servicos_pb2.CreateUpdate(chave=cm[1], valor=cm[2]))
        return retorno

    def run(self):
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

    server = Server(bits, srv, cAnt, cAtu, cSuc, pAnt, pAtu, pSuc)
    server.run()

if __name__ == '__main__':
    run_server()