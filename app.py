# Importando partes do Flask (framework web em Python)
from flask import Flask, render_template, request, jsonify

# Importando datetime para trabalhar com datas (tipo pegar o horário atual)
from datetime import datetime

# Criando a aplicação Flask
app = Flask(__name__)

# Simulação de Banco de Dados (um dicionário em memória)
# Aqui NÃO é um banco real tipo MySQL ou MongoDB
# É só uma variável que guarda dados enquanto o programa está rodando
carteiras = {}

# --- FUNÇÕES LÓGICAS ---
# Aqui fica a "inteligência" do sistema (regras de negócio)


def adicionar_gasto_logica(nome_banco, valor, categoria, descricao):
    # Se o banco ainda não existir no dicionário, cria uma lista vazia
    if nome_banco not in carteiras:
        carteiras[nome_banco] = []

    # --- INTELIGÊNCIA DE ÍCONES ---
    # Converte o nome para minúsculo para facilitar comparação
    nome_low = nome_banco.lower()

    # Ícone padrão (caso não entre em nenhum if)
    icone_banco = "fa-credit-card"

    # Aqui estamos usando IF para identificar qual banco é
    if "nubank" in nome_low:
        icone_banco = "fa-square-n"
    elif "inter" in nome_low:
        icone_banco = "fa-building-columns"
    elif "bradesco" in nome_low:
        icone_banco = "fa-building"
    elif "pix" in nome_low:
        icone_banco = "fa-bolt"

    # --- LÓGICA DE AGRUPAMENTO ---
    # Aqui usamos o next() para procurar um gasto já existente
    # Ele percorre a lista e tenta achar um item com a mesma descrição
    # Se não encontrar, retorna None (ou seja, "nada encontrado")
    item_existente = next(
        (g for g in carteiras[nome_banco]
         if g['desc'].lower() == descricao.lower()),
        None
    )

    # Se encontrou um item com mesma descrição
    if item_existente:
        # Soma o valor no gasto já existente
        item_existente['valor'] += float(valor)
    else:
        # Se não encontrou, cria um novo gasto
        carteiras[nome_banco].append({
            "valor": float(valor),  # float = número decimal (ex: 10.50)
            "desc": descricao,
            "categoria": categoria,
            "data": datetime.now(),  # pega data/hora atual
            "icone_banco": icone_banco,

            # Condicional inline (tipo um if dentro da linha)
            # Se valor > 100 → "Gasto alto", senão → "Ok"
            "status": "Gasto alto" if float(valor) > 100 else "Ok"
        })


def gerar_dashboard():
    # --- PEGAR TODOS OS VALORES ---
    # Aqui usamos list comprehension (forma compacta de criar lista)
    todos_valores = [g["valor"] for lista in carteiras.values() for g in lista]

    # sum() soma todos os valores da lista
    total = sum(todos_valores)

    # --- DESCOBRIR QUAL BANCO GASTOU MAIS ---
    maior_gasto_valor = 0
    cartao_mais_caro = "Nenhum"

    # Percorre cada banco e seus gastos
    for banco, gastos in carteiras.items():
        # Soma os gastos de cada banco
        total_banco = sum(g['valor'] for g in gastos)

        # Se esse banco gastou mais que o anterior
        if total_banco > maior_gasto_valor:
            maior_gasto_valor = total_banco
            cartao_mais_caro = banco

    # --- SIMULAÇÃO DE PROCV (tipo Excel) ---
    # Procurar um gasto específico chamado "aluguel"
    busca_aluguel = "Não encontrado"

    for lista in carteiras.values():
        for g in lista:
            if g["desc"].lower() == "aluguel":
                busca_aluguel = f"R$ {g['valor']:.2f}"

    # Retorna um dicionário com os dados do dashboard
    return {
        "total_geral": total,
        "hoje": total,
        "busca": busca_aluguel,
        "cartao_lider": cartao_mais_caro,
        "valor_lider": maior_gasto_valor
    }


# --- ROTAS FLASK ---
# Rotas são os "endereços" do sistema (tipo páginas ou APIs)

@app.route('/')
def index():
    # Gera os dados do dashboard
    resumo_data = gerar_dashboard()

    # render_template envia dados para o HTML
    return render_template('index.html', carteiras=carteiras, resumo=resumo_data)


@app.route('/api/add', methods=['POST'])
def api_add():
    # request.json pega os dados enviados pelo front-end (JavaScript)
    data = request.json

    # Chama a função lógica para adicionar gasto
    adicionar_gasto_logica(
        data['banco'], data['valor'], data['cat'], data['desc']
    )

    # jsonify retorna um JSON (resposta da API)
    return jsonify({"status": "ok"})


@app.route('/api/delete_banco', methods=['POST'])
def delete_banco():
    data = request.json

    # get() evita erro caso a chave não exista (diferente de data['banco'])
    nome_banco = data.get('banco')

    # Se o banco existir, remove
    if nome_banco in carteiras:
        del carteiras[nome_banco]

    return jsonify({"status": "ok"})


@app.route('/api/delete_gasto', methods=['POST'])
def delete_gasto():
    data = request.json
    nome_banco = data.get('banco')
    index_gasto = data.get('index')

    # Verifica se o banco existe E se o índice é válido
    if nome_banco in carteiras and 0 <= index_gasto < len(carteiras[nome_banco]):
        # remove o gasto da lista (tipo array)
        carteiras[nome_banco].pop(index_gasto)

        # Se não tiver mais gastos, remove o banco inteiro
        if not carteiras[nome_banco]:
            del carteiras[nome_banco]

    return jsonify({"status": "ok"})


# --- INICIALIZAÇÃO DO SERVIDOR ---
# Esse if garante que o código só rode se o arquivo for executado diretamente
if __name__ == '__main__':
    # debug=True faz o servidor reiniciar automaticamente quando você altera o código
    app.run(debug=True)
