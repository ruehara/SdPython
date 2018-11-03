class Config(object):
    def __init__(self):
        self.config = open("config.cfg","r")
        self.host = self.config.readline().split("=")
        self.host = self.host[1]
        self.minport = self.config.readline().split("=")
        self.minport = self.minport[1]
        self.maxport = self.config.readline().split("=")
        self.maxport = self.maxport[1]
        self.maxclients = self.config.readline().split("=")
        self.maxclients = int(self.maxclients[1])
        self.config.close()
    
    def getHost(self):
        return self.host

    def getMinPort(self):
        return self.minport

    def getMaxPort(self):
        return self.maxport    

    def getMaxClient(self):
        return self.maxclients