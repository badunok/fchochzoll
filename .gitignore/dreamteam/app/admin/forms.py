
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Mannschaft, Position


class MannschaftForm(FlaskForm):
    """
    Mannschaft bearbeiten
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Liga', validators=[DataRequired()])
    submit = SubmitField('OK')


class PositionForm(FlaskForm):
    """
    Position bearbeiten
    """
    name = StringField('Position', validators=[DataRequired()])
    description = StringField('Beschreibung', validators=[DataRequired()])
    submit = SubmitField('OK')


class SpielerForm(FlaskForm):
    """
    Spieler bearbeiten
    """
    mannschaft = QuerySelectField(query_factory=lambda: Mannschaft.query.all(),
                                  get_label="name")
    position = QuerySelectField(query_factory=lambda: Position.query.all(),
                                get_label="name")
    submit = SubmitField('OK')
