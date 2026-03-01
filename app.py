import os
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

# -------------------------------
# Conexão com MongoDB
# -------------------------------

mongo_uri = os.environ.get("MONGO_URL") # >> USAR NO RAILWAY    
# mongo_uri = "mongodb://localhost:27017"
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
# Todas as mensagens que o Python envia para o front-end
# -------------------------------
# Withdrawal requested successfully!
# Please enter your PayPal email address.
# Insufficient balance for withdrawal.
# Invalid amount.
# Session expired.
# Daily limit reached.
# Username created successfully.
# Username already exists.
# Passwords do not match.
# Invalid username or password.

# -------------------------------
# Perguntas e imagens aleatórias
# -------------------------------
ASKMUSIC = [
    "Did the music evoke any emotion in you?",
    "Did you like the singer’s voice?",
    "Would you listen to this song again?",
    "Does the lyrics convey a relevant or interesting message?",
    "Did the music production feel well done?",
    "Would you recommend this song to someone?",
    "Did the chorus stick in your head?",
    "Did the song remind you of a moment in your life?",
    "Does the song’s style match your personal taste?",
    "Does the artist seem to have a unique identity?",
    "Did you feel authenticity in the performance?",
    "Is the song different from what you usually listen to?",
    "Did the rhythm make you want to dance or move?",
    "Do you think this song has the potential to become a hit?",
    "Did the cover art or the artist’s image positively catch your attention?",
    "Are the lyrics easy to understand and follow?",
    "Would you listen to this song at different times of the day?",
    "Did the song make you want to learn more about the artist?",
    "Does the song convey genuine feelings?",
    "Is the melody pleasant to listen to?",
    "Was there any part of the song that stood out to you?",
    "Does the music video (if available) enhance the experience?",
    "Do you think the artist is consistent with their other songs?",
    "Is the song original compared to others in the same genre?",
    "Did the rhythm or musical arrangement positively grab your attention?",
    "Can you imagine adding this song to one of your playlists?",
    "Do you think the artist is talented?",
    "Did the song surprise you in any way?",
    "Do you believe the artist has a future in the music industry?",
    "Would you recommend this song or artist to someone with different musical tastes than yours?"
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
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    if password != confirm_password:
        return render_template('login.html', error="Passwords do not match.")
    db_data = load_db()
    if username in db_data['users']:
        return render_template('login.html', error="Username already exists.")
    db_data['users'][username] = {
        "password": password,
        "paypal": "",
        "balance": 43.4,
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
    return render_template('login.html', success="Username created successfully.")

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
            return jsonify(success=False, error="Daily limit reached.")
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
        return jsonify(success=False, error="Session expired.")
    db_data = load_db()
    username = session['username']
    user = db_data['users'][username]
    amount = float(request.form.get('amount'))
    paypal = request.form.get('paypal')
    if abs(amount - user['balance']) > 0.01:
        return jsonify(success=False, error="Invalid amount.")
    if amount < 2000:
        return jsonify(success=False, error="Insufficient balance for withdrawal.")
    if not user['paypal'] and paypal:
        user['paypal'] = paypal
    elif not paypal:
        return jsonify(success=False, error="Please enter your PayPal email address.")
    user['withdrawn'] += user['balance']
    user['balance'] = 0.0
    user['withdrawn_requests'].append({
        "amount": amount,
        "status": "pending",
        "date": datetime.now().isoformat()
    })
    save_db(db_data)
    return jsonify(success=True, message="Withdrawal requested successfully!")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# -------------------------------
# Execução local
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


