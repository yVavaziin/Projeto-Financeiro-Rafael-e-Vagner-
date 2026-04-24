// Gerencia a visibilidade dos campos conforme a escolha do usuário
function alternarModoBanco() {
    const modo = document.getElementById('seletor-banco-modo').value;
    const areaExistente = document.getElementById('area-existente');
    const areaNovo = document.getElementById('area-novo');

    // Se for PIX ou Vazio, esconde os campos extras
    if (modo === 'existente') {
        areaExistente.style.display = 'block';
        areaNovo.style.display = 'none';
    } else if (modo === 'novo') {
        areaExistente.style.display = 'none';
        areaNovo.style.display = 'block';
    } else {
        areaExistente.style.display = 'none';
        areaNovo.style.display = 'none';
    }
}

// Envia os dados para o Flask (Back-end)
function enviarGasto() {
    const modo = document.getElementById('seletor-banco-modo').value;
    let nomeBanco = "";

    // Decide qual nome de banco enviar baseado no modo
    if (modo === 'existente') {
        nomeBanco = document.getElementById('banco-lista').value;
    } else if (modo === 'novo') {
        nomeBanco = document.getElementById('banco-novo').value;
    } else if (modo === 'pix') {
        nomeBanco = "PIX"; // Nome fixo para lançamentos via PIX
    }

    // Validação de segurança
    if (!nomeBanco || !document.getElementById('desc').value || !document.getElementById('valor').value) {
        alert("Ops! Preencha todos os campos antes de lançar.");
        return;
    }

    const dados = {
        banco: nomeBanco,
        desc: document.getElementById('desc').value,
        valor: document.getElementById('valor').value,
        cat: document.getElementById('cat').value
    };

    fetch('/api/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    }).then(() => {
        window.location.reload(); // Atualiza a tela para mostrar o novo card e o relatório
    });
}

// Função para cancelar o cartão inteiro (e todos os seus gastos)
function deletarBanco(nome) {
    if (confirm(`Atenção: Deseja realmente cancelar o cartão ${nome}? Isso apagará todos os gastos registrados nele.`)) {
        fetch('/api/delete_banco', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ banco: nome })
        }).then(() => window.location.reload());
    }
}

// Função para apagar apenas uma linha do extrato
function deletarGasto(banco, index) {
    fetch('/api/delete_gasto', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ banco: banco, index: index })
    }).then(() => window.location.reload());
}   
function verificarOutros() {
    const selectCat = document.getElementById('cat');
    const areaOutros = document.getElementById('area-outros');
    
    if (selectCat.value === 'Outros') {
        areaOutros.style.display = 'block';
    } else {
        areaOutros.style.display = 'none';
    }
}