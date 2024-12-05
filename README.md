# 30112024_API_OS

Questa è un'API RESTful sviluppata con Flask per la gestione di utenti, ordini, prodotti e stati. Include funzionalità di autenticazione, gestione dei carrelli e aggiornamenti dello stato degli ordini.

## **Struttura del Progetto**

- **app/**: Contiene il codice principale dell'applicazione.
- **instance/**: File di configurazione specifici per l'ambiente (es. database).
- **config.py**: Configurazioni dell'applicazione.
- **requirements.txt**: Elenco delle dipendenze richieste.
- **reset.py**: Script per reimpostare e ripopolare il database.
- **run.py**: Entry point per avviare l'applicazione.

---

## **Requisiti**

- **Python 3.x**
- **Flask**
- Moduli specificati in `requirements.txt`

---

## **Installazione**

### **1. Clona il Repository**
Clona il repository dal tuo account GitHub:
```bash
git clone https://github.com/TUO_USERNAME/30112024_API_OS.git
cd 30112024_API_OS

### **Crea un Ambiente Virtuale**
Crea e attiva un ambiente virtuale:

Windows:
bash
Copia codice
python -m venv venv
venv\Scripts\activate
Linux/Mac:
bash
Copia codice
python3 -m venv venv
source venv/bin/activate
3. Installa le Dipendenze
Installa i moduli richiesti:

bash
Copia codice
pip install -r requirements.txt
Configurazione
Crea un file .env nella directory principale e aggiungi le seguenti variabili:

env
Copia codice
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tuo_segreto
DATABASE_URL=sqlite:///instance/database.db
Assicurati che la configurazione del database in config.py corrisponda al tuo ambiente.

Esecuzione dell'Applicazione
Avvia il server Flask:
bash
Copia codice
flask run
Accedi all'applicazione tramite il browser all'indirizzo:
arduino
Copia codice
http://127.0.0.1:5000
API Endpoint
Utenti
GET /users: Recupera tutti gli utenti.
POST /users: Crea un nuovo utente.
PUT /users/<id>: Aggiorna un utente esistente.
DELETE /users/<id>: Elimina un utente.
Ordini
GET /orders: Recupera tutti gli ordini.
POST /orders: Crea un nuovo ordine.
PUT /orders/<id>: Aggiorna un ordine esistente.
DELETE /orders/<id>: Elimina un ordine.
Prodotti
GET /products: Recupera tutti i prodotti.
POST /products: Crea un nuovo prodotto (solo admin).
PUT /products/<id>: Aggiorna un prodotto esistente.
DELETE /products/<id>: Elimina un prodotto (solo admin).
Test
Puoi testare l'API usando:

Postman o Insomnia
cURL:
bash
Copia codice
curl -X GET http://127.0.0.1:5000/users