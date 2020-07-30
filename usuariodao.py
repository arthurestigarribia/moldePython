#-* coding: utf8 -*#-

from usuario import *
import psycopg2

class UsuarioDAO:
    # Inicia o banco de dados
    def __init__(self):
        self.dbname = "usuarios"
        self.host = "localhost"
        self.port = "5432"
        self.user = "postgres"
        self.password = "postgres"

    # Cria a tabela
    def cria(self):
        try:
            con = psycopg2.connect("dbname=" + self.dbname + " host=" + self.host + " port=" + self.port + " user=" + self.user + " password=" + self.password)
            
            cur = con.cursor()

            cur.execute("CREATE TABLE IF NOT EXISTS usuarios(id SERIAL NOT NULL PRIMARY KEY, nome VARCHAR(1000) NOT NULL, email VARCHAR(1000) NOT NULL, senha VARCHAR(32) NOT NULL)")

            con.commit()
            cur.close()
            con.close()

            print('Operacao bem-sucedida.')
        except Exception as e:
            print('Erro na operacao: ' + str(e))

    # Adiciona o registro de usuário
    def adiciona(self, usuario):
        try:
            con = psycopg2.connect("dbname=" + self.dbname + " host=" + self.host + " port=" + self.port + " user=" + self.user + " password=" + self.password)
            
            cur = con.cursor()

            cur.execute("INSERT INTO usuarios(nome, email, senha) VALUES(%s, %s, MD5(%s))", [usuario.nome, usuario.email, usuario.senha])

            con.commit()
            cur.close()
            con.close()

            print('Operacao bem-sucedida.')
        except Exception as e:
            print('Erro na operacao: ' + str(e))
    
    # Remove o registro de usuário
    def remove(self, id):
        try:
            con = psycopg2.connect("dbname=" + self.dbname + " host=" + self.host + " port=" + self.port + " user=" + self.user + " password=" + self.password)
            
            cur = con.cursor()

            cur.execute("DELETE FROM usuarios WHERE id = %s", [id])

            con.commit()
            cur.close()
            con.close()

            print('Operacao bem-sucedida.')
        except Exception as e:
            print('Erro na operacao: ' + str(e))
    
    # Mostra os registros dos usuários
    def lista(self):
        try:
            con = psycopg2.connect("dbname=" + self.dbname + " host=" + self.host + " port=" + self.port + " user=" + self.user + " password=" + self.password)
            
            cur = con.cursor()

            cur.execute("SELECT * FROM usuarios")

            v = cur.fetchall()
            v2 = []

            for i in v:
                v2.append(Usuario(int(i[0]), i[1], i[2], i[3]))

            con.commit()
            cur.close()
            con.close()

            print('Operacao bem-sucedida.')

            return v2
        except Exception as e:
            print('Erro na operacao: ' + str(e))
    
    # Mostra os registros dos usuários
    def lista_um(self):
        try:
            con = psycopg2.connect("dbname=" + self.dbname + " host=" + self.host + " port=" + self.port + " user=" + self.user + " password=" + self.password)
            
            cur = con.cursor()

            cur.execute("SELECT * FROM usuarios")

            v = cur.fetchone()
            v2 = Usuario(int(v[0]), v[1], v[2], v[3])

            con.commit()
            cur.close()
            con.close()

            print('Operacao bem-sucedida.')

            return v2
        except Exception as e:
            print('Erro na operacao: ' + str(e))
    
    # Edita o registro do usuário
    def edita(self, usuario, id):
        try:
            con = psycopg2.connect("dbname=" + self.dbname + " host=" + self.host + " port=" + self.port + " user=" + self.user + " password=" + self.password)
            
            cur = con.cursor()

            cur.execute("UPDATE usuarios SET nome = %s, email = %s, senha = MD5(%s) WHERE id = %s", [usuario.nome, usuario.email, usuario.senha, id])

            con.commit()
            cur.close()
            con.close()

            print('Operacao bem-sucedida.')
        except Exception as e:
            print('Erro na operacao: ' + str(e))