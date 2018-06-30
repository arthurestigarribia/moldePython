#-* coding: utf-8 -*#-

class Usuario:
    def __init__(self, nome, email, senha):
        self.__nome = nome
        self.__email = email
        self.__senha = senha
    
    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id = id

    def getNome(self):
        return self.__nome

    def getEmail(self):
        return self.__email
    
    def getSenha(self):
        return self.__senha

    def setNome(self, nome):
        self.__nome = nome
    
    def setEmail(self, email):
        self.__email = email
    
    def setSenha(self, senha):
        self.__senha = senha

    def __repr__(self):
        return self.getNome() + ";" + self.getEmail()

    def toString(self):
        return self.__repr__()