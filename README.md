# PIT WALL

**Formula 1 Team Data Platform** — progetto finale classe 5M, anno 2026.

PIT WALL è una piattaforma web collaborativa per team di Formula 1. Ogni team dispone di uno spazio privato dove i propri tecnici possono gestire setup vettura, strategie di gara, telemetrie e analisi tecniche per ogni circuito del calendario F1.

---

## Funzionalità

| Modulo | Descrizione |
|---|---|
| **Autenticazione** | Registrazione con codice invito team, login/logout, hashing password |
| **Hub / Bacheca** | Dashboard team con accesso rapido a tutti i contenuti |
| **Circuiti** | Catalogo pubblico dei 24 circuiti F1 con dati tecnici e layout |
| **Post / Analisi** | Creazione e condivisione di analisi tecniche con allegati (immagini, PDF, CSV) |
| **Setup Vettura** | Gestione parametri aerodinamica, sospensioni, freni e pressioni gomme |
| **Strategia Gara** | Pianificazione stint con gomme e giri; validato sui giri effettivi del circuito |
| **Commenti** | Discussione tecnica su ogni post del team |
| **Gestione Team** | Invito, rimozione e promozione dei membri (solo admin) |

---

## Stack tecnologico

- **Backend** — Python 3.12 / Flask 3.0 con architettura Blueprint
- **Database** — SQLite via Flask-SQLAlchemy (ORM)
- **Autenticazione** — Flask-Login + Werkzeug password hashing
- **Frontend** — HTML5, CSS3 vanilla, JavaScript vanilla
- **Configurazione** — python-dotenv per variabili d'ambiente

---

## Requisiti

- Python 3.10+
- pip

---

## Installazione e avvio

```bash
# 1. Clona il repository
git clone https://github.com/AngeloBerlini/final_project.git
cd final_project

# 2. Crea e attiva l'ambiente virtuale
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Configura le variabili d'ambiente
copy .env.example .env       # poi modifica SECRET_KEY

# 5. Avvia l'applicazione
python run.py
```

L'app sarà disponibile su `http://127.0.0.1:5000`.

Al primo avvio il database viene creato automaticamente e i 24 circuiti F1 vengono inseriti.

---

## Configurazione (.env)

```
SECRET_KEY=cambia-questa-chiave-in-produzione
DATABASE_URL=sqlite:///pitwall.db
UPLOAD_FOLDER=app/uploads
MAX_CONTENT_LENGTH=10485760
```

---

## Struttura del progetto

```
final_project/
├── app/
│   ├── auth/           # Registrazione e login
│   ├── circuits/       # Catalogo circuiti (pubblico)
│   ├── comments/       # Commenti ai post
│   ├── hub/            # Bacheca del team
│   ├── media/          # Upload e download file
│   ├── posts/          # Analisi tecniche
│   ├── profile/        # Profilo utente
│   ├── setup/          # Setup vettura
│   ├── strategy/       # Strategie di gara
│   ├── team/           # Gestione team (admin)
│   ├── static/
│   │   ├── css/        # Foglio di stile
│   │   └── circuits/   # Layout tracciati (PNG)
│   ├── templates/      # Template Jinja2
│   ├── models.py       # Modelli SQLAlchemy
│   ├── utils.py        # Utility (upload file)
│   └── __init__.py     # Factory dell'app
├── instance/           # Database SQLite (generato, non versionato)
├── config.py           # Configurazione Flask
├── run.py              # Entry point
├── requirements.txt
└── documento_requisiti.md
```

---

## Primo accesso

1. Accedi a `/auth/register`
2. Inserisci username, email, password e un codice invito
3. Il primo utente di un codice diventa automaticamente **Team Admin**
4. L'admin può gestire i membri dalla sezione **Team**
