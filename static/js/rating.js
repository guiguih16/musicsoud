const myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
var youwin = document.getElementById('youwin');
var audio = new Audio('./static/mp3/cash.mp3');
var numberModal = document.getElementById("numberModal")

async function salvarAvaliacao() {
    try {
      const response = await fetch('/salvar-avaliacoes', {
        method: 'POST'
      });

      const data = await response.json();

      if (data.success) {
        return true
      } else {
        console.log('Erro: ' + data.error);
      }

    } catch (err) {
      console.error('Erro na requisição:', err);
      alert('Ocorreu um erro ao salvar a avaliação. Tente novamente.');
    }
}

function increaseSaldo(v) {
    numberModal.textContent = v
    var increment = 0.05;
    var interval = 10; // Tempo em milissegundos entre cada incremento
    var finalAmount = parseInt(document.getElementById('number-wallet').textContent) + v;
    var receivedAmount = parseInt(document.getElementById('number-wallet').textContent);
    var receivedAmountElement = document.getElementById('number-wallet');
    
    var timer = setInterval(function() {
        receivedAmount += increment;
        receivedAmountElement.textContent = receivedAmount.toFixed(2);
        
        if (receivedAmount >= finalAmount) {
            clearInterval(timer);
            receivedAmountElement.textContent = finalAmount.toFixed(2);
        }
    }, interval);
}

async function proximaAvaliacao(i) {

    youwin.style.display = 'block'
    increaseSaldo(7.50)
    audio.play();
    await salvarAvaliacao()

    setTimeout(() => {
        document.getElementById('rating-' + i).style.display = 'none';
        let proximo = i + 1;

        youwin.style.display = 'none'

        if (document.getElementById('rating-' + proximo)) {
            document.getElementById('rating-' + proximo).style.display = 'block';
            iniciarContagem('rating-timer-' + proximo, 'rating-' + proximo);
        } else {
            myModal.show()
        }
    }, 3000);
}


function iniciarContagem(classRating, containerId) {

    const container = document.getElementById(containerId);
    if (!container) return;

    // 🔒 Apenas botões desse card
    const botoes = container.querySelectorAll('button');
    botoes.forEach(btn => btn.disabled = true);

    const span = container.querySelector(`.${classRating}`);
    let segundos = 1;

    span.textContent = `Please wait ${segundos} seconds to rate`;

    const intervalo = setInterval(() => {
        segundos--;
        span.textContent = `Please wait ${segundos} seconds to rate`;

        if (segundos <= 0) {
            clearInterval(intervalo);
            span.textContent = '';
            botoes.forEach(btn => btn.disabled = false);
        }
    }, 1000);
}

document.addEventListener('DOMContentLoaded', () => {
    iniciarContagem('rating-timer-0', 'rating-0');
});
