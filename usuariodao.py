#-* coding: utf-8 -*#-

from usuario import Usuario
import os
import psycopg2

class UsuarioDAO:
    def create(self):
        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            cur.execute("CREATE TABLE IF NOT EXISTS usuarios(id SERIAL NOT NULL PRIMARY KEY, nome VARCHAR(1000) NOT NULL, email VARCHAR(1000) NOT NULL, senha VARCHAR(32) NOT NULL);")
            
            print "Tabela criada"
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()

    def select(self):
        vetObj = []

        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            cur.execute("SELECT * FROM usuarios")
            vet = cur.fetchall()

            for linha in vet:
                i = linha[0]
                nome = linha[1]
                email = linha[2]
                senha = linha[3]

                u = Usuario(nome, email, senha)
                u.setId(i)

                vetObj.append(u)
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()
        
        return vetObj

    def selectOne(self, id):
        vetObj = []

        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            data = [id]

            cur.execute("SELECT * FROM usuarios WHERE id = %s", data)
            vet = cur.fetchall()

            for linha in vet:
                i = linha[0]
                nome = linha[1]
                email = linha[2]
                senha = linha[3]

                u = Usuario(nome, email, senha)
                u.setId(i)

                vetObj.append(u)
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()

        return vetObj[0]
    
    def selectDados(self, email, senha):
        vetObj = []

        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            data = [email, senha]

            cur.execute("SELECT * FROM usuarios WHERE email = %s AND senha = MD5(%s)", data)
            vet = cur.fetchall()

            for linha in vet:
                i = linha[0]
                nome = linha[1]
                email = linha[2]
                senha = linha[3]

                u = Usuario(nome, email, senha)
                u.setId(i)

                vetObj.append(u)
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()

        return vetObj[0]

    def existeDados(self, email, senha):
        vetObj = []

        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            data = [email, senha]

            cur.execute("SELECT * FROM usuarios WHERE email = %s AND senha = MD5(%s)", data)
            vet = cur.fetchall()
            
            for linha in vet:
                i = linha[0]
                nome = linha[1]
                email = linha[2]
                senha = linha[3]

                u = Usuario(nome, email, senha)
                u.setId(i)

                vetObj.append(u)
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()

        return len(vetObj) > 0

    def existe(self, usuario):
        vetObj = []

        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            data = [usuario.getEmail(), usuario.getSenha()]

            cur.execute("SELECT * FROM usuarios WHERE email = %s AND senha = MD5(%s)", data)
            vet = cur.fetchall()
            
            for linha in vet:
                i = linha[0]
                nome = linha[1]
                email = linha[2]
                senha = linha[3]

                u = Usuario(nome, email, senha)
                u.setId(i)

                vetObj.append(u)
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()

        return len(vetObj) > 0

    def lastId(self):
        last_id = 0

        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            cur.execute("SELECT MAX(id) FROM usuarios")
            vet = cur.fetchall()

            for linha in vet:
                last_id = linha[0]    
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()

        return last_id

    def insert(self, usuario):
        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            data = [usuario.getNome(), usuario.getEmail(), usuario.getSenha()]

            if not self.existe(usuario):
                cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, MD5(%s));", data)
                conn.commit()

                print "Usuário inserido"
            else:
                print "Usuário já existente"
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()

    def delete(self, id):
        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            data = [id]

            cur.execute("DELETE FROM usuarios WHERE id = %s", data)
            conn.commit()

            print "Usuário excluído"
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()
    
    def update(self, usuario, id):
        try:
            conn = psycopg2.connect("dbname=teste host=localhost user=postgres password=postgres")
            cur = conn.cursor()

            data = [usuario.getNome(), usuario.getEmail(), usuario.getSenha(), id]

            if not self.existe(usuario):
                cur.execute("UPDATE usuarios SET nome = %s, email = %s, senha = MD5(%s) WHERE id = %s", data)
                conn.commit()

                print "Usuário editado"
            else:
                print "Usuário inexistente"
        except Exception as e:
            print "Erro[" + str(e) + "]"
        
        cur.close()
        conn.close()