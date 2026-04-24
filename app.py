from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Simulação de Banco de Dados
carteiras = {}

# --- FUNÇÕES LÓGICAS ---


def adicionar_gasto_logica(nome_banco, valor, categoria, descricao):
    if nome_banco not in carteiras:
        carteiras[nome_banco] = []

    nome_low = nome_banco.lower()
    icone_banco = "fa-credit-card"

    if "nubank" in nome_low:
        icone_banco = "fa-square-n"
    elif "inter" in nome_low:
        icone_banco = "fa-building-columns"
    elif "bradesco" in nome_low:
        icone_banco = "fa-building"
    elif "pix" in nome_low:
        icone_banco = "fa-bolt"

    item_existente = next(
        (g for g in carteiras[nome_banco]
         if g['desc'].lower() == descricao.lower()),
        None
    )

    if item_existente:
        item_existente['valor'] += float(valor)
    else:
        carteiras[nome_banco].append({
            "valor": float(valor),
            "desc": descricao,
            "categoria": categoria,
            "data": datetime.now(),
            "icone_banco": icone_banco,
            "status": "Gasto alto" if float(valor) > 100 else "Ok"
        })


def gerar_dashboard():
    todos_valores = [g["valor"] for lista in carteiras.values() for g in lista]
    total = sum(todos_valores)

    maior_gasto_valor = 0
    cartao_mais_caro = "Nenhum"

    for banco, gastos in carteiras.items():
        total_banco = sum(g['valor'] for g in gastos)
        if total_banco > maior_gasto_valor:
            maior_gasto_valor = total_banco
            cartao_mais_caro = banco

    busca_aluguel = "Não encontrado"
    for lista in carteiras.values():
        for g in lista:
            if g["desc"].lower() == "aluguel":
                busca_aluguel = f"R$ {g['valor']:.2f}"

    return {
        "total_geral": total,
        "hoje": total,
        "busca": busca_aluguel,
        "cartao_lider": cartao_mais_caro,
        "valor_lider": maior_gasto_valor
    }

# --- ROTAS FLASK ---


@app.route('/')
def index():
    resumo_data = gerar_dashboard()
    return render_template('index.html', carteiras=carteiras, resumo=resumo_data)


@app.route('/api/add', methods=['POST'])
def api_add():
    data = request.json
    adicionar_gasto_logica(
        data['banco'], data['valor'], data['cat'], data['desc'])
    return jsonify({"status": "ok"})


@app.route('/api/delete_banco', methods=['POST'])
def delete_banco():
    data = request.json
    nome_banco = data.get('banco')
    if nome_banco in carteiras:
        del carteiras[nome_banco]
    return jsonify({"status": "ok"})


@app.route('/api/delete_gasto', methods=['POST'])
def delete_gasto():
    data = request.json
    nome_banco = data.get('banco')
    index_gasto = data.get('index')

    if nome_banco in carteiras and 0 <= index_gasto < len(carteiras[nome_banco]):
        carteiras[nome_banco].pop(index_gasto)
        if not carteiras[nome_banco]:
            del carteiras[nome_banco]

    return jsonify({"status": "ok"})


# --- INICIALIZAÇÃO ÚNICA ---
if __name__ == '__main__':
    # Usando a porta 5001 para evitar conflito com AirPlay no macOS
    app.run(debug=True, port=5001)
