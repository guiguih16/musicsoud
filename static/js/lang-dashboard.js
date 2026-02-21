// Traduções por idioma
const translations = {
    'pt': {
        'saldo-currency': 'Saldo atual',
        'legends-saldo-currency': 'Disponível para retirar',
        'analysis': 'Saques em análises',
        'legends-analysis': 'Aguardando aprovação',
        'avaluations': 'Avaliações',
        'legendas-avaluations': 'Realizadas hoje',
        'limit-day-alert': 'Limite diário de avaliações atingida! Volte amanhã para continuar.',
        'wait': 'AGUARDE',
        'do-avaluations': 'FAZER AVALIAÇÕES',
        'receit': 'Faturamento',
        'legends-receit': 'Gerado hoje',
        'staticBackdropLabel': 'Saldo insuficiente!',
        'do-saque': 'REALIZAR SAQUE'
    },
    'es': {
        'saldo-currency': 'Saldo actual',
        'legends-saldo-currency': 'Disponible para retirar',
        'analysis': 'Retiros en análisis',
        'legends-analysis': 'Esperando aprobación',
        'avaluations': 'Evaluaciones',
        'legendas-avaluations': 'Realizadas hoy',
        'limit-day-alert': '¡Límite diario de evaluaciones alcanzado! Vuelve mañana para continuar.',
        'wait': 'ESPERA',
        'do-avaluations': 'HACER EVALUACIONES',
        'receit': 'Facturación',
        'legends-receit': 'Generado hoy',
        'staticBackdropLabel': '¡Saldo insuficiente!',
        'do-saque': "REALIZAR RETIRO"
    },
    'it': {
        'saldo-currency': 'Saldo attuale',
        'legends-saldo-currency': 'Disponibile per il prelievo',
        'analysis': 'Prelievi in analisi',
        'legends-analysis': 'Tempo medio di approvazione: 5-7 giorni lavorativi',
        'avaluations': 'Valutazioni',
        'legendas-avaluations': 'Effettuate oggi',
        'limit-day-alert': 'Limite giornaliero di valutazioni raggiunto! Torna domani per continuare.',
        'wait': 'ATTENDERE',
        'do-avaluations': 'EFFETTUA VALUTAZIONI',
        'receit': 'Fatturazione',
        'legends-receit': 'Generato oggi',
        'staticBackdropLabel': 'Saldo insufficiente!',
        'do-saque': 'EFFETTUA PRELIEVO'
    }
};

// Função para aplicar as traduções com base no idioma
function applyTranslation(lang) {
    const dict = translations[lang];
    if (!dict) return;

    for (const id in dict) {
        const el = document.getElementById(id);
        if (el) {
            if (el.tagName === 'INPUT') {
                el.placeholder = dict[id];
            } else {
                el.textContent = dict[id];
            }
        }
    }
}

// Exemplo de uso
document.addEventListener('DOMContentLoaded', () => {
    applyTranslation('it'); // Altere para 'pt', 'es', etc.
});
