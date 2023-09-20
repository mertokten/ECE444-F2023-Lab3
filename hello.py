from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import email
from flask import Flask, render_template, session, redirect, url_for, flash

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()]) 
    mail = EmailField('What is your UofT Email address?', validators=[InputRequired(), email()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST']) 
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_mail = session.get('mail')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!') 
        session['name'] = form.name.data
        if old_mail is not None and old_mail != form.mail.data:
            flash('Looks like you changed your email!')
            session['mail'] = form.mail.data
        
        domain = form.mail.data.split('@')[1]
        if 'utoronto' not in domain:
            session['mail'] = None
            session['uoft'] = 3
        else:
            session['mail'] = form.mail.data
            session['uoft'] = 1
        return redirect(url_for('index'))
    if 'uoft' in session:
        uoft = session.get('uoft')
    else:
        uoft = 0
    return render_template('index.html', form = form, name = session.get('name'), mail = session.get('mail'), uoft = uoft)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

@app.route('/clear')
def clear_session():
    session.clear()
    return redirect(url_for('index'))