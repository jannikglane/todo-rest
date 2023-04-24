import uuid
from flask import Flask, render_template, request

# initialisiere Flask-Server
app = Flask(__name__)

# definiere Route für Hauptseite
@app.route('/', 'index')
def index():
    # gebe Antwort an aufrufenden Client zurück
    return "nothing here"

if __name__ == '__main__':
    # starte Flask-Server
    app.run(host='0.0.0.0', port=4200, debug=True)