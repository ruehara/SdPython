import banco

class Log:
    def __init__(self, intervalo, id): 
        self.intervalo = intervalo
        self.id = id
        self.bd = banco.Banco()
    
    def salva_log(self):
        #log.writelines(requisicao +"\n")
        pass