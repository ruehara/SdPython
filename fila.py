class Fila(object):
    def __init__(self):
        self.dados = []

    def insere(self, elemento):
        try:
            self.dados.append(elemento) #insere no final da fila
            return True
        except:
            return False

    def retira(self):
        try:
            if not self.vazia():
                return self.dados.pop() #retira na posicao 0 da fila
        except:
            return None

    def vazia(self):
        return len(self.dados) == 0