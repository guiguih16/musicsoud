// Traduções por idioma
const translations = {
    'pt': {
        'title-form': 'Entre na sua conta para continuar',
        'login': 'Entrar',
        'to-register': 'Cadastre-se',
        'create-account': 'Criar Conta',
        'to-login': 'Faça Login',
        'username': 'Nome de usuário',
        'password': 'Senha',
        'confirm-password': 'Senha',
        'confirm-username': 'Nome de usuário',
        'confirm-confirm-password': 'Confirmar senha'
    },
    'es': {
        'title-form': 'Inicia sesión para continuar',
        'login': 'Iniciar sesión',
        'to-register': 'Regístrate',
        'create-account': 'Crear cuenta',
        'to-login': 'Inicia sesión',
        'username': 'Nombre de usuario',
        'password': 'Contraseña',
        'confirm-password': 'Confirmar contraseña',
        'confirm-username': 'Nombre de usuario',
        'confirm-confirm-password': 'Confirmar contraseña'
    },
    'it': {
        'title-form': 'Accedi per continuare',
        'login': 'Accedi',
        'to-register': 'Registrati',
        'create-account': 'Crea account',
        'to-login': 'Accedi',
        'username': 'Nome utente',
        'password': 'Password',
        'confirm-password': 'Conferma password',
        'confirm-username': 'Nome utente',
        'confirm-confirm-password': 'Conferma password'
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
    applyTranslation('it'); // Troque para 'es', 'en', etc.
});
