from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from .. models import Spieler


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        spieler = Spieler(email=form.email.data,
                            username=form.username.data,
                            vorname=form.vorname.data,
                            nachname=form.nachname.data,
                            password=form.password.data)

        # Spieler zur DB hinzufuegen
        db.session.add(spieler)
        db.session.commit()
        flash('Du hast dich erfolgreich registriert! Weiter zum Login!')

        # >> Login
        return redirect(url_for('auth.login'))

    # template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # Pruefen, ob Spieler bereits vorhanden
        # Und ob das Passwort ok ist
        spieler = Spieler.query.filter_by(email=form.email.data).first()
        if spieler is not None and spieler.verify_password(
                form.password.data):
            # Spieler Login
            login_user(spieler)

            # >> Dashboard
            if spieler.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # Falsches Passwort
        else:
            flash('Falsche Email oder falsches Passwort.')

    # template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du bist raus!')

    # zurueck
    return redirect(url_for('auth.login'))
