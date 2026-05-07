const form = document.getElementById("loginForm");

form.addEventListener("submit", function(e) {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value.trim();

  if (email === "" || senha === "") {
    alert("Preencha todos os campos!");
    return;
  }

  let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];

  const usuario = usuarios.find(u => 
    u.email === email && u.senha === senha
  );

  if (usuario) {

    localStorage.setItem("logado", "true");
    localStorage.setItem("usuarioLogado", email);

    alert("Login realizado com sucesso!");

    // 👉 agora vai pro dashboard
    window.location.href = "dashboard.html";

  } else {
    alert("Email ou senha incorretos!");
  }
});