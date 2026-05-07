<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Bancos de dados temporários (listas)
usuarios = []
transacoes = []
cartoes = []

# ================= ROTAS DE PÁGINAS =================

@app.route('/')
def index():
    return render_template('login.html')
=======
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

>>>>>>> 79115adf9ec84925c87e829d4fc80166185d3f8c

@app.route('/login')
def login():
    return render_template('login.html')

<<<<<<< HEAD
=======

>>>>>>> 79115adf9ec84925c87e829d4fc80166185d3f8c
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

<<<<<<< HEAD
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ================= API =================

@app.route('/api/login', methods=['POST'])
def api_login():
=======

if __name__ == '__main__':
    app.run(debug=True)
    from flask import Flask, request, jsonify

app = Flask(__name__)

usuarios = []
transacoes = []
cartoes = []

# ================= LOGIN =================


@app.route('/login', methods=['POST'])
def login():
>>>>>>> 79115adf9ec84925c87e829d4fc80166185d3f8c
    data = request.json

    for user in usuarios:
        if user['email'] == data['email'] and user['senha'] == data['senha']:
            return jsonify({"status": "ok", "nome": user['nome']})

    return jsonify({"status": "erro"}), 401


<<<<<<< HEAD
@app.route('/api/cadastro', methods=['POST'])
def api_cadastro():
    data = request.json

    for user in usuarios:
        if user['email'] == data['email']:
            return jsonify({"status": "email já existe"}), 400

    usuarios.append(data)
    return jsonify({"status": "ok"})
=======
# ================= CADASTRO =================
@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.json

    usuarios.append(data)

    return jsonify({"status": "cadastrado"})


# ================= ADICIONAR CARTÃO =================
>>>>>>> 79115adf9ec84925c87e829d4fc80166185d3f8c
@app.route('/cartao', methods=['POST'])
def adicionar_cartao():
    data = request.json
    cartoes.append(data)
    return jsonify({"status": "ok"})

<<<<<<< HEAD
@app.route('/transacao', methods=['POST'])
def adicionar_transacao():
=======

# ================= ADICIONAR TRANSAÇÃO =================
@app.route('/transacao', methods=['POST'])
def transacao():
>>>>>>> 79115adf9ec84925c87e829d4fc80166185d3f8c
    data = request.json
    transacoes.append(data)
    return jsonify({"status": "ok"})

<<<<<<< HEAD
@app.route('/dados', methods=['GET'])
def pegar_dados():
=======

# ================= LISTAR DADOS =================
@app.route('/dados', methods=['GET'])
def dados():
>>>>>>> 79115adf9ec84925c87e829d4fc80166185d3f8c
    return jsonify({
        "cartoes": cartoes,
        "transacoes": transacoes
    })

<<<<<<< HEAD
# O comando run fica SEMPRE no final e apenas uma vez
if __name__ == '__main__':
    app.run(debug=True)
=======

app.run(debug=True)
>>>>>>> 79115adf9ec84925c87e829d4fc80166185d3f8c
