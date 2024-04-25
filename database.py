from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dein_sehr_geheimer_schluessel'

# Anmeldeinformationen für die MongoDB
mongodb_username = 'rent-a-room-service-user'
mongodb_password = 'sml12345'
mongodb_host = 'localhost'
mongodb_port = 27017
mongodb_auth_source = 'admin'

# MongoDB-Verbindung mit Anmeldeinformationen
mongodb_uri = f'mongodb://{mongodb_username}:{mongodb_password}@{mongodb_host}:{mongodb_port}/?authSource={mongodb_auth_source}'
client = MongoClient(mongodb_uri)

# Datenbank und Sammlung auswählen
db = client['rent-a-room']
collection = db.rooms

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['email'] = request.form['email']
        return redirect(url_for('home'))
    return render_template('login.html')




@app.route('/')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    # ... Der Rest deiner Home-Logik ...

    rooms = collection.find(
        {'$or': [
            {'bewohner_ids': {'$exists': False}},
            {'bewohner_ids': {'$size': 0}}
        ]},
        {'name': 1}
    )
    return render_template('index.html', rooms=rooms)

@app.route('/room/<id>')
def room(id):
    room = collection.find_one({'_id': ObjectId(id)})
    return dumps(room)

@app.route('/update-room/<id>', methods=['POST'])





def update_room(id):
    room_data = request.json
    # Formatierung der Daten von Strings zu Datumsobjekten
    gebucht_von = datetime.strptime(room_data['gebucht_von'], '%Y-%m-%d')
    gebucht_bis = datetime.strptime(room_data['gebucht_bis'], '%Y-%m-%d')
    bewohner = room_data['bewohner_ids'].split(',')  # Nehme an, dass die IDs durch Kommas getrennt sind

    # Aktualisiere das Dokument in der Datenbank
    result = collection.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'gebucht_von': gebucht_von,
            'gebucht_bis': gebucht_bis,
            'bewohner_ids': bewohner
        }}
    )

    return jsonify({'success': result.modified_count > 0})

@app.route('/account')
def account():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']

    # Hole die Personendaten aus der "persons"-Collection
    person = db.persons.find_one({"_id": email})
    if not person:
        return "Person nicht gefunden", 404

    # Suche nach Räumen, bei denen die Person entweder Besitzer oder Bewohner ist.
    rooms_owned = list(collection.find({"besitzer_id": email}))
    rooms_rented = list(collection.find({"bewohner_ids": email}))

    # Render das Template und übergebe die Person und die Raumdaten
    return render_template('account.html', person=person, rooms_owned=rooms_owned, rooms_rented=rooms_rented)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))




@app.route('/update-account', methods=['POST'])
def update_account():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    # Extrahiere die aktualisierten Daten aus dem Formular
    updated_data = {
        'vorname': request.form['vorname'],
        'nachname': request.form['nachname'],
        'alter': int(request.form['alter']),
        'geschlecht': request.form['geschlecht'],
        'telefon': request.form['telefon'],
    }

    # Aktualisiere die Daten in der 'persons'-Collection
    db.persons.update_one({'_id': email}, {'$set': updated_data})


    return redirect(url_for('account'))



@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_room = {
            "name": request.form['name'],
            "beschreibung": request.form['beschreibung'],
            "adresse": request.form['adresse'],
            "zimmer": int(request.form['zimmer']),
            "fläche": float(request.form['fläche']),
            "besitzer_id": session['email'],
            # Initialisiere 'bewohner_ids' als leere Liste
            "bewohner_ids": []
        }
        
        # Füge den neuen Raum zur 'rooms'-Collection hinzu
        db.rooms.insert_one(new_room)
        return redirect(url_for('home'))  # Oder eine Bestätigungsseite anzeigen
    
    else:
        email = session['email']
        owned_rooms = list(db.rooms.find({"besitzer_id": email}))

    return render_template('sell.html', owned_rooms=owned_rooms)



if __name__ == '__main__':
    app.run(debug=True)
