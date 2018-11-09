from __future__ import print_function
import sys
import threading
import time
import grpc
import servicos_pb2
import servicos_pb2_grpc
import fila
import config
from colorama import init
init()

class Client:
    def __init__(self):
        self.configuracao = config.Config()
        self.host = self.configuracao.getHost().strip("\n")

    def main(self):
        try:
            porta = input("Porta do Servidor: ")
            self.channel = grpc.insecure_channel(self.host+":"+porta)
            crud = threading.Thread(target=self.crud_thread, name="crud")
            crud.start()
        except:
            print("Erro ao iniciar crud_thread")

    def print_menu(self):
        print("1 - Create Ex: 1 123 ABCD")
        print("2 - Read   Ex: 2 123")
        print("3 - Update Ex: 3 123 EFGH")
        print("4 - Delete Ex: 4 123")
        print("5 - Sair   Ex: 5")

    def crud_thread(self):
        ativo = True
        self.print_menu()
        stub = servicos_pb2_grpc.RequisicaoStub(self.channel)
        ret = stub.Conectado(servicos_pb2.Hello(chave = "teste"))
        print(ret.resposta)
        while ativo:
            entrada = input("Comando: ")
            temp = entrada.split(' ',2)
            while temp[0] != '5':
                if self.validar_temp(entrada):
                    if temp[0] == '1':
                        retorno  = stub.Create.future(servicos_pb2.CreateUpdate(chave=temp[1], valor=temp[2]))
                    elif temp[0] == '2':
                        retorno = stub.Read.future(servicos_pb2.ReadDelete(chave=temp[1]))
                    elif temp[0] == '3':
                        retorno = stub.Update.future(servicos_pb2.CreateUpdate(chave=temp[1], valor=temp[2]))
                    elif temp[0] == '4':
                        retorno = stub.Delete.future(servicos_pb2.ReadDelete(chave=temp[1]))
                    retorno.add_done_callback(self.resposta)
                else:
                    print("Comando não reconhecido")
                entrada = input("Comando: ")
                temp = entrada.split(' ',2)
            ativo = False

    def validar_temp(self,entrada):
        msg = entrada.split(' ',2)
        try:
            if int(msg[0]) >= 1 and int(msg[0]) <= 5 and isinstance(int(msg[1]),int):
                return True
            else:
                return False
        except:
            return False

    def resposta(self,retorno):
        res = retorno.result()
        if res.resposta is not None:
            if res.resposta == 'NOK' or res.resposta == 'Chave não existe!':
                print('\033[31m'+res.resposta+'\033[37m' )
            else:
                print('\033[32m'+res.resposta+'\033[37m' )

if __name__ == '__main__':
    client = Client()
    client.main()