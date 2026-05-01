from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


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
    data = request.json

    for user in usuarios:
        if user['email'] == data['email'] and user['senha'] == data['senha']:
            return jsonify({"status": "ok", "nome": user['nome']})

    return jsonify({"status": "erro"}), 401


# ================= CADASTRO =================
@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.json

    usuarios.append(data)

    return jsonify({"status": "cadastrado"})


# ================= ADICIONAR CARTÃO =================
@app.route('/cartao', methods=['POST'])
def adicionar_cartao():
    data = request.json
    cartoes.append(data)
    return jsonify({"status": "ok"})


# ================= ADICIONAR TRANSAÇÃO =================
@app.route('/transacao', methods=['POST'])
def transacao():
    data = request.json
    transacoes.append(data)
    return jsonify({"status": "ok"})


# ================= LISTAR DADOS =================
@app.route('/dados', methods=['GET'])
def dados():
    return jsonify({
        "cartoes": cartoes,
        "transacoes": transacoes
    })


app.run(debug=True)
