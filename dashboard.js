let contas = JSON.parse(localStorage.getItem("contas")) || [];
let transacoes = JSON.parse(localStorage.getItem("transacoes")) || [];

const email = localStorage.getItem("usuarioLogado");
let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];
const usuario = usuarios.find(u => u.email === email);

// USER
if (usuario) {
  document.getElementById("nomeUsuario").innerText = usuario.nome;
}

// FOTO
document.getElementById("uploadFoto").addEventListener("change", e => {
  const reader = new FileReader();
  reader.onload = () => {
    localStorage.setItem("foto", reader.result);
    document.getElementById("fotoPerfil").src = reader.result;
  };
  reader.readAsDataURL(e.target.files[0]);
});

document.getElementById("fotoPerfil").src = localStorage.getItem("foto");

// PERFIL
function salvarPerfil() {
  usuario.nome = document.getElementById("nomePerfil").value;
  localStorage.setItem("usuarios", JSON.stringify(usuarios));
}

// CONTAS
function abrirModal() {
  document.getElementById("modal").style.display = "block";
}

function salvarConta() {
  const nome = nomeConta.value;
  const tipo = tipoConta.value;
  const saldo = parseFloat(saldoConta.value);

  contas.push({ nome, tipo, saldo });
  localStorage.setItem("contas", JSON.stringify(contas));

  renderContas();
}

function renderContas() {
  const div = document.getElementById("contas");
  div.innerHTML = "";

  contas.forEach(c => {
    div.innerHTML += `
      <div class="card">
        <h4>${c.nome}</h4>
        <p>Saldo: R$ ${c.saldo}</p>
        <button onclick="novaTransacao('${c.nome}')">Movimentar</button>
      </div>
    `;
  });
}

// TRANSAÇÕES
function novaTransacao(contaNome) {
  const valor = prompt("Valor:");
  const tipo = prompt("entrada ou saida");

  const conta = contas.find(c => c.nome === contaNome);

  if (tipo === "entrada") {
    conta.saldo += parseFloat(valor);
  } else {
    conta.saldo -= parseFloat(valor);
  }

  transacoes.push({ conta: contaNome, valor, tipo });
  localStorage.setItem("contas", JSON.stringify(contas));
  localStorage.setItem("transacoes", JSON.stringify(transacoes));

  renderTudo();
}

// EXTRATO
function renderTransacoes() {
  const filtro = filtroTipo.value;
  const ul = document.getElementById("extrato");
  ul.innerHTML = "";

  let lista = transacoes;

  if (filtro !== "todos") {
    lista = transacoes.filter(t => t.tipo === filtro);
  }

  lista.forEach(t => {
    ul.innerHTML += `<li>${t.tipo} - R$ ${t.valor}</li>`;
  });
}

// RESUMO
function resumo() {
  let total = 0, entradas = 0, saidas = 0;

  transacoes.forEach(t => {
    if (t.tipo === "entrada") entradas += parseFloat(t.valor);
    if (t.tipo === "saida") saidas += parseFloat(t.valor);
  });

  contas.forEach(c => total += c.saldo);

  totalEl.innerText = "R$ " + total;
  entradasEl.innerText = "R$ " + entradas;
  saidasEl.innerText = "R$ " + saidas;
}

// GRÁFICOS
function graficos() {
  new Chart(graficoPizza, {
    type: "doughnut",
    data: {
      labels: contas.map(c => c.nome),
      datasets: [{ data: contas.map(c => c.saldo) }]
    }
  });

  new Chart(graficoLinha, {
    type: "line",
    data: {
      labels: transacoes.map((_, i) => i+1),
      datasets: [{ data: transacoes.map(t => t.valor) }]
    }
  });
}

// INIT
function renderTudo() {
  renderContas();
  renderTransacoes();
  resumo();
}

renderTudo();
graficos();

function logout() {
  localStorage.clear();
  window.location.href = "index.html";
}
function toggleGraficos() {
  const box = document.getElementById("graficosBox");
  box.classList.toggle("hidden");
}

function mostrarPizza() {
  document.getElementById("graficoPizza").style.display = "block";
  document.getElementById("graficoLinha").style.display = "none";

  new Chart(graficoPizza, {
    type: "doughnut",
    data: {
      labels: contas.map(c => c.nome),
      datasets: [{ data: contas.map(c => c.saldo) }]
    }
  });
}

function mostrarLinha() {
  document.getElementById("graficoLinha").style.display = "block";
  document.getElementById("graficoPizza").style.display = "none";

  new Chart(graficoLinha, {
    type: "line",
    data: {
      labels: transacoes.map((_, i) => i+1),
      datasets: [{ data: transacoes.map(t => t.valor) }]
    }
  });
}