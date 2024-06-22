from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Advice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advice_text = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_advice/<id_num>')
def get_advice(id_num):
    url = f'https://api.adviceslip.com/advice/{id_num}'
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json()
        advice = content.get("slip", {}).get("advice")
        if advice:
            new_advice = Advice(advice_text=advice)
            db.session.add(new_advice)
            db.session.commit()
            flash(f'Successfully added new advice: "{advice}"', 'success')
        else:
            flash('Advice not found for this ID.', 'error')
    else:
        flash('Failed to retrieve advice from API.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
