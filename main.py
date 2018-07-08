#-* coding: utf-8 -*#-

from usuario import Usuario
from usuariodao import UsuarioDAO
from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib

app = Flask(__name__)

@app.route('/index')
def index():
    if 'id' in session:
        return render_template("index.html", nome = session['nome'], logado = True)
    else:
        return render_template("index.html", logado = False)

@app.route('/sair')
def sair():
    session.pop('id', None)
    session.pop('nome', None)
    session.pop('email', None)
    session.pop('senha', None)

    return redirect(url_for('index'))

@app.route('/excluir')
def excluir():
    UsuarioDAO().delete(session['id'])

    return redirect(url_for('logout'))

@app.route('/login')
def paginaLogin(erro = ""):
    if 'id' in session:
        return redirect(url_for('index'))
    elif erro != 0:
        return render_template("login.html", error=erro)
    else:
        return render_template("login.html", error="")

@app.route('/rotaLogin', methods=['GET', 'POST'])
def rotaLogin():
    if request.method == 'POST':
        if UsuarioDAO().existeDados(request.form['Email'], request.form['Senha']):
            u = UsuarioDAO().selectDados(request.form['Email'], request.form['Senha'])

            session['id'] = u.getId()
            session['nome'] = u.getNome()
            session['email'] = request.form['Email']

            return redirect(url_for('index'))
        
        else:
            return paginaLogin("Usuario ou senha incorretos.")
    else:
        return paginaLogin("")

@app.route('/cadastro')
def paginaCadastro(erro = ""):
    if 'id' in session:
        return redirect(url_for('index'))
    elif erro != 0:
        return render_template("cadastro.html", error=erro)
    else:
        return render_template("cadastro.html", error="")

@app.route('/rotaCadastro', methods=['GET', 'POST'])
def rotaCadastro():
    if request.method == 'POST':
        u = Usuario(request.form['Nome'], request.form['Email'], request.form['Senha'])

        if (not UsuarioDAO().existe(u)) and (request.form['Nome'] and request.form['Email'] and request.form['Senha']):
            UsuarioDAO().insert(u)

            session['id'] = UsuarioDAO().lastId()
            session['nome'] = request.form['Nome']
            session['email'] = request.form['Email']

            return redirect(url_for('index'))
        else:
            return paginaCadastro("Cadastro nao efetuado.")
    else:
        return paginaCadastro("")

@app.route('/editar')
def paginaEditar(erro = ""):
    if not ('id' in session):
        return redirect(url_for('login'))
    elif erro != 0:
        return render_template("editar.html", logado=True, nome = session['nome'], error=erro)
    else:
        return render_template("editar.html", logado=True, nome = session['nome'], error="")

@app.route('/rotaEditar', methods=['GET', 'POST'])
def rotaEditar():
    if request.method == 'POST':
        u = Usuario(request.form['Nome'], request.form['Email'], request.form['Senha'])

        if (not UsuarioDAO().existe(u)) and (request.form['Nome'] and request.form['Email'] and request.form['Senha']):

            UsuarioDAO().update(u, session['id'])

            session['nome'] = request.form['Nome']
            session['email'] = request.form['Email']

            return redirect(url_for('index'))
        else:
            return paginaEditar("Edicao nao realizada.")
    else:
        return paginaEditar("")

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'AKSJDHFGPQOWIEURYTMZNXBCVL0192837465'
    app.run()