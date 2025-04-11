var bntSingin = document.querySelector("#singin");
var bntSingup = document.querySelector("#singup");
var body = document.querySelector("body");

bntSingin.addEventListener("click", function() {
    body.className = 'sing-in-js'
});

bntSingup.addEventListener('click', function(){
    body.className = 'sing-up-js'
});



document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form[action*="cadastro"]');
  const senhaInput = form.querySelector('input[name="senha"]');
  const confirmaSenhaInput = form.querySelector('input[name="confirmaSenha"]');
  const telefoneInput = form.querySelector('input[name="telefone"]');
  const cpfInput = form.querySelector('input[name="cpf"]');

  // Mensagem personalizada
  const mostrarErro = (input, mensagem) => {
    let feedback = input.nextElementSibling;
    if (!feedback || !feedback.classList.contains('feedback')) {
      feedback = document.createElement('small');
      feedback.className = 'feedback';
      input.parentNode.appendChild(feedback);
    }
    feedback.innerHTML = mensagem;
    feedback.style.color = '#d32f2f';
  };

  const limparErro = (input) => {
    let feedback = input.nextElementSibling;
    if (feedback && feedback.classList.contains('feedback')) {
      feedback.textContent = '';
    }
  };

  // Máscara de telefone simples
  telefoneInput.addEventListener('input', () => {
    let v = telefoneInput.value.replace(/\D/g, '');
    if (v.length > 2) v = '(' + v.slice(0, 2) + ') ' + v.slice(2);
    if (v.length > 9) v = v.slice(0, 9) + '-' + v.slice(9);
    telefoneInput.value = v.slice(0, 14);
  });

  form.addEventListener('submit', (e) => {
    let valido = true;

    // Verifica CPF/CNPJ
    const cpf = cpfInput.value.replace(/\D/g, '');
    if (cpf.length !== 11 && cpf.length !== 14) {
      mostrarErro(cpfInput, 'Insira um CPF (11 dígitos) ou CNPJ (14 dígitos) válido.');
      valido = false;
    } else {
      limparErro(cpfInput);
    }

    // Verifica senha
    const senha = senhaInput.value;
    const senhaForte = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+[\]{}|\\:;'",.<>/?`~]).{8,}$/;
    if (!senhaForte.test(senha)) {
      mostrarErro(senhaInput, 'A senha precisa ter no mínimo 8 caracteres, 1 letra maiúscula, 1 número e 1 caractere especial.');
      valido = false;
    } else {
      limparErro(senhaInput);
    }

    // Confirmação da senha
    if (senha !== confirmaSenhaInput.value) {
      mostrarErro(confirmaSenhaInput, 'As senhas não coincidem!');
      valido = false;
    } else {
      limparErro(confirmaSenhaInput);
    }

    if (!valido) {
      e.preventDefault();
    }
  });
});

const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');

requiredFields.forEach(field => {
  // Define mensagem personalizada se o campo estiver vazio
  field.addEventListener('invalid', function () {
    this.setCustomValidity(`Por favor, preencha o campo "${getFieldLabel(this)}" corretamente.`);
  });

  // Limpa a mensagem personalizada ao começar a digitar
  field.addEventListener('input', function () {
    this.setCustomValidity('');
  });
});

// Função para tentar pegar o label associado ao input
function getFieldLabel(input) {
  const label = document.querySelector(`label[for="${input.id}"]`);
  return label ? label.innerText.replace(/:$/, '') : 'obrigatório';
}

document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);
  const erro = urlParams.get('erro');

  if (erro === 'email') {
      Swal.fire({
          icon: 'error',
          title: 'Erro!',
          text: 'Este e-mail já está cadastrado. Tente outro!',
          confirmButtonText: 'Entendi',
          confirmButtonColor: '#00796B'
      });
  } else if (erro === 'perfil') {
      Swal.fire({
          icon: 'error',
          title: 'Erro!',
          text: 'Erro ao definir perfil. Tente novamente.',
          confirmButtonText: 'Entendi',
          confirmButtonColor: '#00796B'
      });
  }
});
