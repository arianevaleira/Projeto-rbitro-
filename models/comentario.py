from models import conectar_db

class Comentario:
        
    @classmethod
    def add_comentario(cls, conteudo, usu_id):
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO tb_comentarios(com_conteudo, com_usu_id) VALUES(%s,%s)", (conteudo, usu_id,))
        conn.commit()
        conn.close()
        cursor.close()
        return True
    
    @classmethod
    def listar(cls):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT usu_nome as usuario, com_conteudo as comentario FROM tb_comentarios JOIN tb_usuarios ON usu_id = com_usu_id")
        comentarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return comentarios
    # def __init__(self, usu_id, conteudo):
    #     self.usu_id = usu_id
    #     self.conteudo = conteudo


    # def add_comentario(self):
    #     conn = conectar_db()
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         "INSERT INTO tb_comentarios (com_conteudo, com_usu_id) VALUES (%s, %s)",
    #         (self.usu_id, self.conteudo)
    #     )
    #     conn.commit()
    #     cursor.close()
    #     conn.close()

    
