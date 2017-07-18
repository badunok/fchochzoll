from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import MannschaftForm, SpielerForm, PositionForm
from .. import db
from ..models import Mannschaft, Spieler, Position


def check_admin():
    # Kein Zugang
    if not current_user.is_admin:
        abort(403)


# Mannschaft Views


@admin.route('/mannschaften', methods=['GET', 'POST'])
@login_required
def list_mannschaften():
    """
    Alle Mannschaften anzeigen
    """
    check_admin()

    mannschaften = Mannschaft.query.all()

    return render_template('admin/mannschaften/mannschaften.html',
                           mannschaften=mannschaften, title="Mannschaften")


@admin.route('/mannschaften/add', methods=['GET', 'POST'])
@login_required
def add_mannschaft():
    """
    Mannschaft zur DB hinzufuegen
    """
    check_admin()

    add_mannschaft = True

    form = MannschaftForm()
    if form.validate_on_submit():
        mannschaft = Mannschaft(name=form.name.data,
                                description=form.description.data)
        try:
            # Mannschaft hinzufuegen
            db.session.add(mannschaft)
            db.session.commit()
            flash('Mannschaft hinzugefuegt.')
        except:
            # wenn Mannschaft schon vorhanden
            flash('Mannschaft bereits vorhanden.')

        # zurueck 
        return redirect(url_for('admin.list_mannschaften'))

    # Template laden
    return render_template('admin/mannschaften/mannschaft.html', action="Add",
                           add_mannschaft=add_mannschaft, form=form,
                           title="Mannschaft hinzufuegen")


@admin.route('/mannschaften/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_mannschaft(id):
    """
    Mannschaft bearbeiten
    """
    check_admin()

    add_mannschaft = False

    mannschaft = Mannschaft.query.get_or_404(id)
    form = MannschaftForm(obj=mannschaft)
    if form.validate_on_submit():
        mannschaft.name = form.name.data
        mannschaft.description = form.description.data
        db.session.commit()
        flash('Mannschaft bearbeitet.')

        # zurueck
        return redirect(url_for('admin.list_mannschaften'))

    form.description.data = mannschaft.description
    form.name.data = mannschaft.name
    return render_template('admin/mannschaften/mannschaft.html', action="Edit",
                           add_mannschaft=add_mannschaft, form=form,
                           mannschaft=mannschaft, title="Mannschaft bearbeiten")


@admin.route('/mannschaften/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_mannschaft(id):
    """
    Mannschaft entfernen
    """
    check_admin()

    mannschaft = Mannschaft.query.get_or_404(id)
    db.session.delete(mannschaft)
    db.session.commit()
    flash('Mannschaft entfernt')

    # zurueck
    return redirect(url_for('admin.list_mannschaften'))

    return render_template(title="mannschaft entfernen")


# Positionen Views


@admin.route('/positionen')
@login_required
def list_positionen():
    check_admin()
    """
    Liste mit allen Positionen
    """
    positionen = Position.query.all()
    return render_template('admin/positionen/positionen.html',
                           positionen=positionen, title='Positionen')


@admin.route('/positionen/add', methods=['GET', 'POST'])
@login_required
def add_position():
    """
    Position hinzufuegen
    """
    check_admin()

    add_position = True

    form = PositionForm()
    if form.validate_on_submit():
        position = Position(name=form.name.data,
                    description=form.description.data)

        try:
            # Position zu DB
            db.session.add(position)
            db.session.commit()
            flash('Position hinzugefuegt')
        except:
            # wenn es die position schon gibt
            flash('Diese Position gibt es schon')

        # zurueck
        return redirect(url_for('admin.list_positionen'))

    # template
    return render_template('admin/positionen/position.html', add_position=add_position,
                           form=form, title='Position hinzufuegen')


@admin.route('/positionen/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_position(id):
    """
    position bearbeiten
    """
    check_admin()

    add_position = False

    position = Position.query.get_or_404(id)
    form = PositionForm(obj=position)
    if form.validate_on_submit():
        position.name = form.name.data
        position.description = form.description.data
        db.session.add(position)
        db.session.commit()
        flash('Position bearbeitet.')

        # zurueck
        return redirect(url_for('admin.list_positionen'))

    form.description.data = position.description
    form.name.data = position.name
    return render_template('admin/positionen/position.html', add_position=add_position,
                           form=form, title="Position bearbeiten")


@admin.route('/positionen/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_position(id):
    """
    Position entfernen
    """
    check_admin()

    position = Position.query.get_or_404(id)
    db.session.delete(position)
    db.session.commit()
    flash('Position entfernt.')

    # zurueck
    return redirect(url_for('admin.list_positionen'))

    return render_template(title="Position entfernen")


# SPieler Views

@admin.route('/spielers')
@login_required
def list_spielers():
    """
    Liste aller Spieler
    """
    check_admin()

    spielers = Spieler.query.all()
    return render_template('admin/spielers/spielers.html',
                           spielers=spielers, title='Spieler')


@admin.route('/spielers/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_spieler(id):
    """
    Mannschaft und Position zuweisen
    """
    check_admin()

    spieler = Spieler.query.get_or_404(id)

    # admin darf nicht selbst zugewiesen werden
    if spieler.is_admin:
        abort(403)

    form = SpielerForm(obj=spieler)
    if form.validate_on_submit():
        spieler.mannschaft = form.mannschaft.data
        spieler.position = form.position.data
        db.session.add(spieler)
        db.session.commit()
        flash('Erfolgreich zugewiesen.')

        # zurueck
        return redirect(url_for('admin.list_spielers'))

    return render_template('admin/spielers/spieler.html',
                           spieler=spieler, form=form,
                           title='Spieler zuweisen')

@admin.route('/spielers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_spieler(id):
    """
    Spieler entfernen
    """
    check_admin()

    spieler = Spieler.query.get_or_404(id)
    db.session.delete(spieler)
    db.session.commit()
    flash('Spieler entfernt')

    # zurueck
    return redirect(url_for('admin.list_spielers'))

    return render_template(title="mannschaft entfernen")
