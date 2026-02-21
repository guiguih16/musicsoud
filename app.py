import os
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import smtplib
from email.message import EmailMessage

# -------------------------------
# Conexão com MongoDB
# -------------------------------
mongo_uri = os.environ.get("MONGO_URL")
if mongo_uri is None:
    raise Exception("MONGO_URL não encontrada no Railway")
client = MongoClient(mongo_uri)

db = client["spotify_rewards"]
collection = db["italian"]

# -------------------------------
# Flask App
# -------------------------------
app = Flask(__name__)
app.secret_key = '4pp_r3w4rd$'  # troque por uma chave segura em produção

# -------------------------------
# Perguntas e imagens aleatórias
# -------------------------------
ASKMUSIC = [
    "La musica ha suscitato qualche emozione in te?",
    "Ti è piaciuta la voce del cantante o della cantante?",
    "Ascolteresti di nuovo questa canzone?",
    "Il testo trasmette un messaggio rilevante o interessante?",
    "La produzione musicale ti è sembrata ben fatta?",
    "Consiglieresti questa canzone a qualcuno?",
    "Il ritornello ti è rimasto in testa?",
    "La canzone ti ha ricordato qualche momento della tua vita?",
    "Lo stile della canzone corrisponde ai tuoi gusti personali?",
    "L’artista sembra avere un’identità propria?",
    "Hai percepito autenticità nell’interpretazione?",
    "La canzone è diversa da ciò che ascolti di solito?",
    "Il ritmo ti ha fatto venire voglia di ballare o muoverti?",
    "La canzone ha il potenziale per diventare un successo?",
    "La copertina o l’immagine dell’artista ha attirato positivamente la tua attenzione?",
    "Il testo è facile da capire e seguire?",
    "Ascolteresti questa canzone in diversi momenti della giornata?",
    "La canzone ti ha lasciato la voglia di conoscere meglio l’artista?",
    "La canzone trasmette qualche sentimento vero?",
    "La melodia è piacevole all’orecchio?",
    "C’è qualche parte della canzone che ti ha colpito particolarmente?",
    "Il videoclip (se presente) migliora l’esperienza?",
    "Credi che l’artista sia coerente con le sue altre canzoni?",
    "La canzone è originale rispetto ad altre dello stesso genere?",
    "Il ritmo o l’arrangiamento musicale ha attirato la tua attenzione in modo positivo?",
    "Ti immagini di aggiungere questa canzone a una delle tue playlist?",
    "Credi che l’artista abbia talento?",
    "La canzone ti ha sorpreso in qualche modo?",
    "Credi che l’artista abbia futuro nell’industria?",
    "Consiglieresti questa canzone o artista a qualcuno con gusti musicali diversi dai tuoi?"
]

IMGSRANDOM = list(range(1, 31))  # imagens de 1 a 30

# -------------------------------
# Funções para MongoDB
# -------------------------------
def load_db():
    """Carrega todo o 'banco' como um dict, igual ao JSON antigo."""
    db_doc = collection.find_one({"_id": "db"})
    if not db_doc:
        db_doc = {"_id": "db", "users": {}}
        collection.insert_one(db_doc)
    db_copy = db_doc.copy()
    db_copy.pop("_id", None)
    return db_copy

def save_db(data):
    """Salva todo o 'banco' no MongoDB, mantendo a mesma estrutura do JSON."""
    collection.update_one({"_id": "db"}, {"$set": data}, upsert=True)

# -------------------------------
# Funções auxiliares
# -------------------------------
def processar_saques_automaticos():
    """Move saques de 'pending' para 'confirmado' após 5 dias"""
    db_data = load_db()
    agora = datetime.now()
    for username, user in db_data['users'].items():
        if 'withdrawn_requests' not in user:
            continue
        novos_pedidos = []
        for req in user['withdrawn_requests']:
            data_pedido = datetime.fromisoformat(req['date'])
            if (agora - data_pedido) >= timedelta(days=5):
                user['total_withdrawn'] = user.get('total_withdrawn', 0.0) + req['amount']
                user['last_withdraw_date'] = req['amount']
                user['withdrawn'] -= req['amount']
            else:
                novos_pedidos.append(req)
        user['withdrawn_requests'] = novos_pedidos
    save_db(db_data)

def resetar_se_novo_dia(user):
    hoje = datetime.now().date().isoformat()
    if user.get('last_evaluation_date') != hoje:
        user['evaluations_today'] = 0
        user['earned_today'] = 0.0
        user['last_evaluation_date'] = hoje

# -------------------------------
# Hooks
# -------------------------------
@app.before_request
def antes_de_toda_requisicao():
    processar_saques_automaticos()

# -------------------------------
# Rotas
# -------------------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db_data = load_db()
        user = db_data['users'].get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Nome utente o password non validi.")
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    if password != confirm_password:
        return render_template('login.html', error="Le password non coincidono.")
    db_data = load_db()
    if username in db_data['users']:
        return render_template('login.html', error="Il nome utente esiste già.")
    db_data['users'][username] = {
        "password": password,
        "paypal": "",
        "balance": 43.40,
        "withdrawn": 0.0,
        "total_withdrawn": 0.0,
        "withdrawn_requests": [],
        "created_at": datetime.now().isoformat(),
        "last_withdraw_date": 0.0,
        "evaluations_today": 0,
        "earned_today": 0.0,
        "last_evaluation_date": datetime.now().date().isoformat()
    }
    save_db(db_data)
    session['username'] = username
    return render_template('login.html', success="Nome utente creato con successo.")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    db_data = load_db()
    username = session['username']
    user = db_data['users'].get(username)
    if not user:
        session.pop('username', None)
        return redirect(url_for('login'))
    today = datetime.now().date().isoformat()
    if user.get("last_evaluation_date") != today:
        user["evaluations_today"] = 0
        user["earned_today"] = 0.0
        user["last_evaluation_date"] = today
        save_db(db_data)
    return render_template('dashboard.html', user=user, username=username)

@app.route('/rating')
def rating():
    if 'username' not in session:
        return redirect(url_for('login'))
    db_data = load_db()
    username = session['username']
    user = db_data['users'][username]
    resetar_se_novo_dia(user)
    if user['evaluations_today'] >= 16 or user['earned_today'] >= 120.0:
        save_db(db_data)
        return redirect(url_for('dashboard'))
    avaliacoes_restantes = 16 - user['evaluations_today']
    perguntas = random.sample(ASKMUSIC, avaliacoes_restantes)
    images = random.sample(IMGSRANDOM, avaliacoes_restantes)
    save_db(db_data)
    return render_template('rating.html', user=user, perguntas=perguntas, images=images, avaliacoes_restantes=avaliacoes_restantes)

@app.route('/salvar-avaliacoes', methods=['POST'])
def salvar_avaliacoes():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        db_data = load_db()
        username = session['username']
        user = db_data['users'][username]
        resetar_se_novo_dia(user)
        if user['evaluations_today'] >= 16 or user['earned_today'] >= 120.0:
            return jsonify(success=False, error="Limite giornaliero raggiunto.")
        user['evaluations_today'] += 1
        user['earned_today'] += 7.5
        user['balance'] += 7.5
        user['last_evaluation_date'] = datetime.now().date().isoformat()
        save_db(db_data)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/confirm-withdraw', methods=['POST'])
def confirm_withdraw():
    if 'username' not in session:
        return jsonify(success=False, error="Sessão expirada.")
    db_data = load_db()
    username = session['username']
    user = db_data['users'][username]
    amount = float(request.form.get('amount'))
    paypal = request.form.get('paypal')
    if abs(amount - user['balance']) > 0.01:
        return jsonify(success=False, error="Valor inválido.")
    if amount < 2000:
        return jsonify(success=False, error="Saldo insuficiente para saque.")
    if not user['paypal'] and paypal:
        user['paypal'] = paypal
    elif not paypal:
        return jsonify(success=False, error="Informe o e-mail do PayPal.")
    user['withdrawn'] += user['balance']
    user['balance'] = 0.0
    user['withdrawn_requests'].append({
        "amount": amount,
        "status": "pending",
        "date": datetime.now().isoformat()
    })
    save_db(db_data)
    return jsonify(success=True, message="Saque solicitado com sucesso!")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    email_recebido = data.get('email')
    print("email_recebido: ", email_recebido)
    remetente = 'info.team.saq@gmail.com'
    destinatario = email_recebido
    assunto = 'Richiesta di rimborso confermata!'
    mensagem = """
    Ti inviamo questa e-mail per confermare che la tua richiesta di rimborso è stata ricevuta correttamente e inoltrata al nostro team finanziario, responsabile dell'elaborazione dello storno.

    L'importo sarà rimborsato integralmente con lo stesso metodo di pagamento utilizzato per l'acquisto, entro un termine massimo di 15 giorni.
    """

    senha = 'ocpt zlxm hete gqkr'

    msg = EmailMessage()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.set_content(mensagem)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
        email.login(remetente, senha)
        email.send_message(msg)

    print("Email enviado com sucesso!")

    return jsonify(success=True)

# -------------------------------
# Execução local
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)




