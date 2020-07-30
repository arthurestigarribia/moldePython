#-* coding: utf8 -*#-

from usuario import *
from usuariodao import *
from flask import *
import hashlib
import os
import sys

app = Flask(__name__)
app.secret_key = "chave_secreta"

udao = UsuarioDAO()

# Obtém o usuário da lista
def getUsuario(email):
    return udao.lista_um()

# Verifica o login
def verificaLogin(email, senha):
    return (getUsuario(email) and hashlib.md5(senha.encode()).hexdigest() == getUsuario(email).senha) == True

# Verifica se o usuário não está logado
@app.before_request
def antesDaRota():
	if not(request.path == '/login' or request.path == '/login' or request.path == '/fazLogin' or request.path == '/fazCadastro') and 'id' not in session:
		return redirect('/login')

# Página inicial
@app.route('/')
def paginaInicial():
    if 'id' in session:
        acao = "/edicao"
        textologin = session['nome']
    else:
        acao = "/login"
        textologin = "Entrar ou cadastrar"

    return render_template("index.html", acao=acao, textologin=textologin, erro=None)

# Página de login
@app.route('/login')
def paginaLogin():
    if 'id' in session:
        acao = "/edicao"
        textologin = session['nome']

        return redirect('/')
    else:
        acao = "/login"
        textologin = "Entrar ou cadastrar"
    
        return render_template("login.html", acao=acao, textologin=textologin, erro=None)

# Faz o login
@app.route('/fazLogin', methods = ['POST'])
def fazLogin():
    email = request.form['email']
    senha = request.form['senha']

    if verificaLogin(email, senha):
        session['nome'] = getUsuario(email).nome
        session['email'] = email
        session['id'] = getUsuario(email).id
    
        return redirect('/')
    else:
        return render_template("login.html", acao="/login", textologin="Entrar ou cadastrar", erro="Login ou senha inválidos.")

# Faz o cadastro
@app.route('/fazCadastro', methods = ['POST'])
def fazCadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    if getUsuario(email) == None:
        u = Usuario(0, nome, email, senha)
        udao.adiciona(u)

        session['nome'] = nome
        session['email'] = email
        session['id'] = getUsuario(email).id

        return redirect('/')
    else:
        return render_template("login.html", acao="/login", textologin="Entrar ou cadastrar", erro="Login ou senha inválidos.")

# Faz o logout
@app.route('/fazLogout')
def fazLogout():
    if 'id' in session:
        session.pop('nome', None)
        session.pop('email', None)

        session.pop('id', None)

        return redirect('/')
    else:
        return redirect('/login')

# Exclui o cadastro
@app.route('/exclui')
def exclui():
    if 'id' in session:
        udao = UsuarioDAO()

        session.pop('nome', None)
        session.pop('email', None)

        udao.remove(session['id'])

        session.pop('id', None)
    
        return redirect('/')
    else:
        return redirect('/login')

# Edita o cadastro
@app.route('/edicao')
def paginaEdicao():
    if 'id' in session:
        acao = "/edicao"
        textologin = session['nome']

        return render_template("edicao.html", nome=session['nome'], email=session['email'], acao=acao, textologin=textologin, erro=None)
    else:
        acao = "/login"
        textologin = "Entrar ou cadastrar"

        return redirect('/login')

# Faz a edição do cadastro
@app.route('/fazEdicao', methods = ['POST'])
def fazEdicao():
    if 'id' in session:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if getUsuario(email) == None or session['id'] == getUsuario(email).id:
            u = Usuario(0, nome, email, senha)
            udao.edita(u, session['id'])

            session['nome'] = nome
            session['email'] = email
        
            return redirect('/')
        else:
            return redirect('/edicao')
    else:
        return redirect('/login')

# Página sobre o molde
@app.route('/sobre')
def sobre():
    if 'id' in session:
        acao = "/edicao"
        textologin = session['nome']

        return render_template("sobre.html", nome=session['nome'], email=session['email'], acao=acao, textologin=textologin, erro=None)
    else:
        acao = "/login"
        textologin = "Entrar ou cadastrar"

        return render_template("sobre.html", nome=None, email=None, acao="/login", textologin="Entrar ou cadastrar", erro=None)

# Erro 404
@app.errorhandler(404)
def erro(e):
    return render_template('404.html'), 404

app.run()
