class Banco(object):
    def __init__(self):
        self.mapa = {}
        
    def create(self, chave, valor):
        try:
            if(self.mapa[chave] is not None):
                return False
        except:
            self.mapa[chave] = valor
            return True

    def read(self, chave):
        try:
            if(self.mapa[chave] is not None):
                return self.mapa[chave]
        except:
            return None
    
    def update(self, chave, novoValor):
        try:
            if(self.mapa[chave] is not None):
                self.mapa[chave] = novoValor
                return True
        except:
            return False

    def delete(self, chave):
        try:
            if(self.mapa[chave] is not None):
                del(self.mapa[chave])
                return True
        except:
            return False