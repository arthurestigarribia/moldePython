#-* coding: utf8 -*#-

class Usuario:
    def __init__(self, id=0, nome="", email="", senha=""):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
    
    def __repr__(self):
        return 'Usuario[nome=' + self.nome + ', email=' + self.email + ']'