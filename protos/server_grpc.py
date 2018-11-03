from concurrent import futures
import grpc
import servicos_pb2
import servicos_pb2_grpc
import threading 
import fila
import banco
import time
import os
import config
import random

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
f1 = fila.Fila()
f2 = fila.Fila()
f3 = fila.Fila()
f4 = fila.Fila()
bd = banco.Banco()

class Requisicao(servicos_pb2_grpc.RequisicaoServicer):
    def Create(self,request,context):
        requisicao = "1 " + request.chave + " " + request.valor
        #tratar responsabilidade
        f1.insere(requisicao)
        

    def Read(self, request, context):
        requisicao = "2 " + request.chave
        f1.insere(requisicao)


    def Update(self, request, context):
        requisicao = "3 " + request.chave + " " + request.valor
        f1.insere(requisicao)
        

    def Delete(self, request, context):
        requisicao = "4 " + request.chave
        f1.insere(requisicao)
        #return servicos_pb2.Resultado(resposta="OK\n")

class Server(object):
    def __init__(self):
        self.antecessor = None
        self.sucessor = None
        self.cfg = config.Config()
        self.host = self.cfg.getHost().strip("\n")
        self.port = random.randint(int(self.cfg.getMinPort().strip("\n")), int(self.cfg.getMaxPort().strip("\n")))
        print("host = " + self.host +"\nport= " + str(self.port))
        
    def main(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        servicos_pb2_grpc.add_RequisicaoServicer_to_server(Requisicao(), server)
        server.add_insecure_port(self.host+':'+str(self.port))
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)

    def duplica_thread(self):
        while True:
            while not f1.vazia():
                try:
                    comando = f1.retira()
                    f2.insere(comando)
                    f3.insere((comando))
                except:
                    pass
    
    def log_thread(self): 
        while True:
            while not f2.vazia():
                pass #
        
    def banco_thread(self):
        while True:
            while not f3.vazia():
                try:
                    cm = f3.retira()
                    cm = str(cm)
                    cm = cm.split(' ',2)
                    ok = False
                    if int(cm[0]) == 1 :
                        if bd.create(int(cm[1]),cm[2]):
                            ok = True
                            msg = "OK"
                    elif int(cm[0]) == 2 :
                            read = bd.read(int(cm[1]))
                            if read:
                                msg = "Chave:" + str(cm[1]) +" Valor: " + read
                                ok = True
                    elif int(cm[0]) == 3 :
                        if bd.update(int(cm[1]),cm[2]):
                            msg = "OK"
                            ok = True
                    elif int(cm[0]) == 4 :
                        if bd.delete(int(cm[1])):
                            msg = "OK"
                            ok = True
                    if not ok:
                        msg = "NOK"
                except:
                    pass
    
    def responder(self,msg):
        return servicos_pb2.Resultado(resposta=msg)

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
    server = Server()
    server.run()

if __name__ == '__main__':
    run_server()