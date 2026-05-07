// Função para facilitar a captura de elementos
const get = (id) => document.getElementById(id);

async function salvarConta() {
    const nomeInput = get("nomeConta");
    const saldoInput = get("saldoConta");

    if (!nomeInput || !saldoInput) {
        console.error("IDs nomeConta ou saldoConta não encontrados no HTML");
        return;
    }

    const nome = nomeInput.value.trim();
    const saldo = parseFloat(saldoInput.value);

    if (!nome || isNaN(saldo)) {
        alert("Por favor, preencha o nome e um valor numérico válido.");
        return;
    }

    // Dados que serão enviados para o Python (app.py)
    const dados = { nome: nome, valor: saldo, tipo: 'entrada' };

    try {
        const resposta = await fetch('/transacao', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        if (resposta.ok) {
            nomeInput.value = "";
            saldoInput.value = "";
            // Recarrega os dados do servidor para atualizar a tela
            await atualizarInterface();
            console.log("Sucesso: Dados enviados ao Python");
        }
    } catch (erro) {
        console.error("Erro de conexão com o servidor:", erro);
        alert("O servidor Python não respondeu. Verifique o terminal do VS Code.");
    }
}

async function atualizarInterface() {
    try {
        const resposta = await fetch('/dados');
        const dados = await resposta.json();
        
        // Atualiza a lista de contas
        const divContas = get("contas");
        if (divContas) {
            divContas.innerHTML = "";
            dados.transacoes.forEach(t => {
                divContas.innerHTML += `
                    <div class="card-item" style="border-bottom: 1px solid #444; padding: 10px;">
                        <strong>${t.nome}</strong>: R$ ${parseFloat(t.valor).toFixed(2)}
                    </div>`;
            });
        }

        // Atualiza o saldo total
        const totalEl = get("total");
        if (totalEl) {
            const soma = dados.transacoes.reduce((acc, t) => acc + parseFloat(t.valor), 0);
            totalEl.innerText = `R$ ${soma.toFixed(2)}`;
        }
    } catch (e) {
        console.log("Erro ao atualizar interface:", e);
    }
}

let meuGrafico = null;

async function gerarGraficos() {
    const resposta = await fetch('/dados');
    const dados = await resposta.json();

    if (dados.transacoes.length === 0) {
        alert("Adicione dados primeiro para gerar o gráfico.");
        return;
    }

    const ctx = get("graficoPizza");
    if (!ctx) return;

    if (meuGrafico) meuGrafico.destroy();

    meuGrafico = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: dados.transacoes.map(t => t.nome),
            datasets: [{
                data: dados.transacoes.map(t => t.valor),
                backgroundColor: ['#6c5ce7', '#00cec9', '#fab1a0', '#fdcb6e']
            }]
        }
    });
}

// Quando a página abrir, busca o que já estiver salvo no Python
window.onload = atualizarInterface;