#-* coding: utf8 -*#-

from usuario import *
from usuariodao import *
from flask import *
import os
import sys

udao = UsuarioDAO()

udao.cria()

u = Usuario(0, 'Nome', 'nome@exemplo.com', 'nome')

udao.adiciona(u)

print(udao.lista())

for i in udao.lista():
    udao.remove(i.id)