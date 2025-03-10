from flask import Flask, redirect, render_template, url_for, request, flash, session
from werkzeug.security import check_password_hash
from models.arbitro import Arbitro
from models.contratante import Contratante
from models.usuario import Usuario
from models.comentario import Comentario
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)

app.config['SECRET_KEY'] = 'muitodificil'


@login_manager.user_loader
def load_user(user_id):
    return Usuario.get(int(user_id))


#primeira pagina (de abertura)
@app.route('/')
def inicial():
    return render_template('index.html')


#Pagina inicial (login)
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = Usuario.get_by_email(email)
        if user and check_password_hash(user['usu_senha'], senha):
            login_user(Usuario.get(user['usu_id']))
            return redirect(url_for('home'))
        
        else:
            flash("Email ou senha inválidos")
    return render_template('login.html')



#Pagina de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        senha = request.form['senha']
        tipo = request.form['tipo']

        if Usuario.exists(email):
            return "Email já cadastrado!", 400
        
        else:
            user = Usuario(nome=nome, email=email, cpf=cpf, telefone=telefone, senha=senha, tipo=tipo)
            user.add_usuario()            
            if tipo == "contratante":
                Contratante.add_contratante(user.get_id())
            else:
                Arbitro.add_arbitro(user.get_id())
            # logar o usuário após cadastro
            login_user(user)
            return redirect(url_for('login'))

    return render_template('login.html')


#Pagina principal (usuario)
@app.route('/home', methods=['GET', 'POST'])
@login_required 
def home():
    comentarios = Comentario.listar()
    return render_template('home.html', comentarios=comentarios)


#Pagina sobre (informações)
@app.route('/sobre')
@login_required
def sobre(): 
    return render_template('sobre.html')


#Pagina Sobre (Fora do Login)
@app.route('/sobre_inicial')
def sobre_inicial():
    return render_template('sobre_inicial.html')

#Pagina de solicitação (Cadastrar partidas)
@app.route('/solicitacao')
@login_required
def solicitacao():
    return render_template('solicitacao.html')


@app.route('/comentarios', methods=['POST'])
@login_required
def comentarios():
    conteudo = request.form['conteudo']
    usu_id = current_user.get_id()
    Comentario.add_comentario(conteudo, usu_id)
    return redirect (url_for('home'))


#Pagina onde ficará a galeria (fotos das partidas)
@app.route('/partidas')
@login_required
def partidas():
    return render_template('partidas.html')

#Pagina onde ficara a alteração de dados do usurio (editar)
@app.route('/configuracoes')
@login_required
def configuracoes():
    return render_template('configuracao.html')


#Pagina onde ficara as notificações do usuario
@app.route('/notificacoes')
@login_required
def notificacoes():
    return render_template('notificacoes.html')

@app.route('/saiba-mais')
def saiba_mais():
    return render_template('saiba_mais.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)
