from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Spieler(UserMixin, db.Model):
    """
    Spieler Tabelle
    """

    # Modelnamen >> singular
    # Tabellennamen >> plural
    __tablename__ = 'spielers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    vorname = db.Column(db.String(60), index=True)
    nachname = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    mannschaft_id = db.Column(db.Integer, db.ForeignKey('mannschaften.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('positionen.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Wenn das Passwort nicht ok ist
        """
        raise AttributeError('Dein Passwort ist nicht ok.')

    @password.setter
    def password(self, password):
        """
        Hash Passwort
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Stimmen Passwort und Email ?
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Spieler: {}>'.format(self.username)


# User laden
@login_manager.user_loader
def load_user(user_id):
    return Spieler.query.get(int(user_id))


class Mannschaft(db.Model):
    """
    Mannschaft Tabelle
    """

    __tablename__ = 'mannschaften'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    spieler = db.relationship('Spieler', backref='mannschaft',
                                lazy='dynamic')

    def __repr__(self):
        return '<Mannschaft: {}>'.format(self.name)


class Position(db.Model):
    """
    Position Tabelle
    """

    __tablename__ = 'positionen'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    spieler = db.relationship('Spieler', backref='position',
                                lazy='dynamic')

    def __repr__(self):
        return '<Position: {}>'.format(self.name)
