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
    },
    'en': {
        'saldo-currency': 'Current balance',
        'legends-saldo-currency': 'Available for withdrawal',
        'analysis': 'Withdrawals under review',
        'legends-analysis': 'Pending approval',
        'avaluations': 'Reviews',
        'legendas-avaluations': 'Completed today',
        'limit-day-alert': 'Daily review limit reached! Come back tomorrow to continue.',
        'wait': 'PLEASE WAIT',
        'do-avaluations': 'DO REVIEWS',
        'receit': 'Revenue',
        'legends-receit': 'Generated today',
        'staticBackdropLabel': 'Insufficient balance!',
        'do-saque': 'WITHDRAW FUNDS',
        'title-last-withdrawl': 'Last withdrawal approved',
        'legends-last-withdrawl': 'International transfers may take up to 5 business days.',
        "alert-withdrawl-value-minin": "To make your first withdrawal, you must have a minimum available balance of €2,000.",
        "comfirn-alert-withdrawl": "I understand",
        "paypal-modal-title": "Enter your PayPal",
        "paypal-current-balance": "Current balance:",
        "paypal-instructions": "To proceed, enter your PayPal email address. If you don’t have one, please create a PayPal account.",
        "paypal-note": "The full amount will be transferred after verification.",
        "paypal-cancel": "Cancel",
        "paypal-confirm": "Confirm Withdrawal"
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
    applyTranslation('en'); // Altere para 'pt', 'es', etc.
});
