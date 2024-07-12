from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///portfolio.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)

# Example JSON data loading
with open('static/data/package-lock.json', 'r') as f:
    json_data = json.load(f)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(150), nullable=True)
    message = db.Column(db.Text, nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)


    def __repr__(self):
        return f'<Contact {self.name}>'

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        if not name or not email or not message:
            flash("Please fill out all required fields", "error")
            return redirect('/')
        
        new_contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()
        
        flash("Your message has been sent successfully!", "success")
        return redirect('/')

    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit.html')
def submit():
    return render_template('submit.html')

@app.route('/machine.html')
def machine():
    return render_template('machine.html')

@app.route('/visual.html')
def visual():
    return render_template('visual.html')

@app.route('/business.html')
def business():
    return render_template('business.html')

@app.route('/json-data', methods=['GET'])
def get_json_data():
    return jsonify(json_data)

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True, port=8000)
