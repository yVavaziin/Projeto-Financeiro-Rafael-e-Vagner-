// ================= NAVBAR LOGIN =================
const logado = localStorage.getItem("logado");
const navButtons = document.querySelector('.nav-buttons');

if (logado === "true") {
  navButtons.innerHTML = `
    <button class="perfil">Meu Perfil</button>
    <button class="logout">Sair</button>
  `;

  document.querySelector('.logout').addEventListener('click', () => {
    localStorage.removeItem("logado");
    window.location.href = "index.html";
  });

} else {
  const btnLogin = document.querySelector('.login');
  const btnCadastro = document.querySelector('.cadastro');

  if (btnLogin) {
    btnLogin.addEventListener('click', () => {
      window.location.href = "login.html"; // ✅ corrigido
    });
  }

  if (btnCadastro) {
    btnCadastro.addEventListener('click', () => {
      window.location.href = "cadastro.html"; // ✅ corrigido
    });
  }
}


// ================= CARROSSEL =================
const track = document.querySelector('.carousel-track');
const cards = document.querySelectorAll('.card');
const carousel = document.querySelector('.carousel');

let index = 0;
let autoPlay;

// cria botões
const btnPrev = document.createElement('button');
const btnNext = document.createElement('button');

btnPrev.innerText = "⟨";
btnNext.innerText = "⟩";

btnPrev.classList.add('nav-btn', 'prev');
btnNext.classList.add('nav-btn', 'next');

if (carousel) {
  carousel.appendChild(btnPrev);
  carousel.appendChild(btnNext);
}

function updateCarousel() {
  if (!cards.length) return;
  const cardWidth = cards[0].offsetWidth + 25;
  track.style.transform = `translateX(-${index * cardWidth}px)`;
}

function nextSlide() {
  if (index < cards.length - 3) {
    index++;
  } else {
    index = 0;
  }
  updateCarousel();
}

function prevSlide() {
  if (index > 0) {
    index--;
  } else {
    index = cards.length - 3;
  }
  updateCarousel();
}

btnNext.addEventListener('click', nextSlide);
btnPrev.addEventListener('click', prevSlide);

// autoplay
function startAutoPlay() {
  autoPlay = setInterval(nextSlide, 3000);
}

function stopAutoPlay() {
  clearInterval(autoPlay);
}

if (carousel) {
  carousel.addEventListener('mouseenter', stopAutoPlay);
  carousel.addEventListener('mouseleave', startAutoPlay);
}

startAutoPlay();


// ================= ANIMAÇÃO SCROLL =================
const sections = document.querySelectorAll('.hero, .carousel-section, .sobre');

function reveal() {
  const trigger = window.innerHeight * 0.85;

  sections.forEach(sec => {
    const top = sec.getBoundingClientRect().top;

    if (top < trigger) {
      sec.classList.add('show');
    }
  });
}

window.addEventListener('scroll', reveal);
reveal();


// ================= CTA =================
const cta = document.querySelector('.cta');

if (cta) {
  cta.addEventListener('click', () => {
    alert("Vamos começar 🚀");
  });
}