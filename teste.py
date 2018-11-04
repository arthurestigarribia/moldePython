#-* coding: utf8 -*#-

from usuario import *
from usuariodao import *
from flask import *
import md5
import os
import sys

udao = UsuarioDAO()

u = Usuario(0, 'Nome', 'nome@exemplo.com', 'nome')

udao.adiciona(u)

print udao.lista()