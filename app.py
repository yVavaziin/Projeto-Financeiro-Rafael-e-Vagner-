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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ================= API =================

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json

    for user in usuarios:
        if user['email'] == data['email'] and user['senha'] == data['senha']:
            return jsonify({"status": "ok", "nome": user['nome']})

    return jsonify({"status": "erro"}), 401


@app.route('/api/cadastro', methods=['POST'])
def api_cadastro():
    data = request.json

    for user in usuarios:
        if user['email'] == data['email']:
            return jsonify({"status": "email já existe"}), 400

    usuarios.append(data)
    return jsonify({"status": "ok"})
@app.route('/cartao', methods=['POST'])
def adicionar_cartao():
    data = request.json
    cartoes.append(data)
    return jsonify({"status": "ok"})

@app.route('/transacao', methods=['POST'])
def adicionar_transacao():
    data = request.json
    transacoes.append(data)
    return jsonify({"status": "ok"})

@app.route('/dados', methods=['GET'])
def pegar_dados():
    return jsonify({
        "cartoes": cartoes,
        "transacoes": transacoes
    })

# O comando run fica SEMPRE no final e apenas uma vez
if __name__ == '__main__':
    app.run(debug=True)
