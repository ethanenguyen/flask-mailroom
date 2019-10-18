import os
import base64
from flask import Flask, render_template, request, redirect, url_for, session, flash
from peewee import DoesNotExist
from model import Donor, Donation 

app = Flask(__name__)  # This line should already be in your main.py
app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            amount = request.form['amount'].strip()
            if not name or not amount:
                raise ValueError("Name or Amount is blank")
            aDonor = Donor.select().where(Donor.name == request.form['name']).get()
            flash('Donor name found.', 'success')
        except DoesNotExist:
            aDonor = Donor(name=request.form['name'])
            aDonor.save()
            flash('Donor name not found. Create a new donor.', 'warning')
        except ValueError:
            flash('Name or Amount is blank. Please try again.', 'error')
            return render_template('create.jinja2')   

        Donation(donor=aDonor, value=request.form['amount']).save()
        return redirect(url_for('all'))       

    else:
        return render_template('create.jinja2')    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

