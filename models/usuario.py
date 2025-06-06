from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from models import conectar_db

class Usuario(UserMixin):
    _hash: str

    def __init__(self, **kwargs):
        self._id = None
        self._cep = None 
        self._nome = kwargs.get('nome')
        self._email = kwargs.get('email')
        self._cpf = kwargs.get('cpf')
        self._telefone = kwargs.get('telefone')
        self._tipo = kwargs.get('tipo')
        self._hash = kwargs.get('hash')
        if 'senha' in kwargs:
            self._senha = kwargs['senha']  
        self._cep = kwargs.get('cep')
        self._cidade = kwargs.get('cidade')
        self._estado = kwargs.get('estado')
        self._latitude = kwargs.get('latitude')
        self._longitude = kwargs.get('longitude')

    def get_id(self):
        return str(self._id)

    @property
    def _senha(self):
        return self._hash

    @_senha.setter
    def _senha(self, senha):
        if senha:  
            self._hash = generate_password_hash(senha)

    def add_usuario(self):
        if not self._hash:  # Se a senha não foi definida
            raise ValueError("Erro: A senha não pode ser nula!")

        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            INSERT INTO tb_usuarios (usu_nome, usu_email, usu_cpf, usu_telefone, usu_senha, usu_tipo, usu_cep, usu_cidade, usu_estado) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (self._nome, self._email, self._cpf, self._telefone, self._hash, self._tipo, self._cep, self._cidade, self._estado))

        self._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @classmethod  
    def get(cls, user_id=None, specific_user_id=None):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        
        if specific_user_id:
            cursor.execute("SELECT * FROM tb_usuarios WHERE usu_id = %s", (specific_user_id,))
        else:
            cursor.execute("SELECT * FROM tb_usuarios WHERE usu_id = %s", (user_id,))
            
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        print(f"Dados do usuário do banco de dados: {user}")
        if user:
            loaduser = Usuario(
                nome=user['usu_nome'],
                email=user['usu_email'],
                cpf=user['usu_cpf'],
                telefone=user['usu_telefone'],
                tipo=user['usu_tipo'],
                hash=user['usu_senha'],
                cep=user['usu_cep'],
                cidade=user['usu_cidade'],
                estado=user['usu_estado'],
                latitude=user.get('usu_latitude'),  
                longitude=user.get('usu_longitude')  
            )
            loaduser._id = user['usu_id']
            return loaduser
        return None

    @classmethod
    def exists(cls, email):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_usuarios WHERE usu_email = %s", (email,))
        user = cursor.fetchall()
        conn.commit()
        conn.close()
        return bool(user)

    @classmethod
    def get_by_email(cls, email):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT usu_id, usu_email, usu_senha, usu_tipo FROM tb_usuarios WHERE usu_email = %s", (email,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        return user
    

   
    @classmethod
    def atualizar_localizacao(cls, user_id, lat, lng):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tb_usuarios 
            SET usu_latitude = %s, usu_longitude = %s 
            WHERE usu_id = %s
        """, (lat, lng, user_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar_localizacoes(cls):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT usu_id, usu_nome, usu_latitude AS lat, usu_longitude AS lng FROM tb_usuarios WHERE usu_latitude IS NOT NULL AND usu_longitude IS NOT NULL")
        localizacoes = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return localizacoes

    @classmethod
    def atualizar(cls, user_id, nome=None, cep=None, estado=None, cidade=None):
        conn = conectar_db()
        cursor = conn.cursor()

        
        updates = []
        parameters = []

        if nome:
            updates.append("usu_nome = %s")
            parameters.append(nome)
        if cep:
            updates.append("usu_cep = %s")
            parameters.append(cep)
        if estado:
            updates.append("usu_estado = %s")
            parameters.append(estado)
        if cidade:
            updates.append("usu_cidade = %s")
            parameters.append(cidade)


        parameters.append(user_id)

        if updates:
            query = f"UPDATE tb_usuarios SET {', '.join(updates)} WHERE usu_id = %s"
            cursor.execute(query, parameters)
            conn.commit()

        cursor.close()
        conn.close()
