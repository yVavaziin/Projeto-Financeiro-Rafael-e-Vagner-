from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

usuarios = []
transacoes = []
cartoes = []

# ================= PÁGINAS =================


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# ================= LOGIN =================

@app.route('/api/login', methods=['POST'])
def api_login():

    data = request.json

    for user in usuarios:

        if (
            user["email"] == data["email"]
            and user["senha"] == data["senha"]
        ):

            return jsonify({
                "status": "ok",
                "mensagem": "Login realizado com sucesso!"
            })

    return jsonify({
        "status": "erro",
        "mensagem": "Email ou senha inválidos"
    }), 401


# ================= CADASTRO =================

@app.route('/api/cadastro', methods=['POST'])
def api_cadastro():

    data = request.json

    usuarios.append(data)

    return jsonify({
        "status": "ok",
        "mensagem": "Usuário cadastrado com sucesso!"
    })


# ================= ADICIONAR CARTÃO =================

@app.route('/cartao', methods=['POST'])
def adicionar_cartao():

    data = request.json

    cartoes.append(data)

    return jsonify({
        "status": "ok",
        "mensagem": "Cartão adicionado com sucesso!"
    })


# ================= ADICIONAR TRANSAÇÃO =================

@app.route('/transacao', methods=['POST'])
def adicionar_transacao():

    data = request.json

    transacoes.append(data)

    return jsonify({
        "status": "ok",
        "mensagem": "Transação adicionada com sucesso!"
    })


# ================= LISTAR DADOS =================

@app.route('/dados', methods=['GET'])
def pegar_dados():

    return jsonify({
        "usuarios": usuarios,
        "cartoes": cartoes,
        "transacoes": transacoes
    })


if __name__ == '__main__':
    app.run(debug=True)
