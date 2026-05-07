const form = document.getElementById('cadastroForm');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const nome = document.getElementById('nome').value.trim();
  const email = document.getElementById('email').value.trim();
  const senha = document.getElementById('senha').value.trim();

  let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];

  // verifica se já existe
  const existe = usuarios.find(user => user.email === email);

  if (existe) {
    alert("Esse email já está cadastrado!");
    return;
  }

  // salva usuário
  usuarios.push({ nome, email, senha });
  localStorage.setItem("usuarios", JSON.stringify(usuarios));

  alert("Cadastro realizado com sucesso!");

  window.location.href = "login.html";
});