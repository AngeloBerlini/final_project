from functools import wraps
from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import User
from app.team import team_bp


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated


@team_bp.route('/')
@login_required
@admin_required
def manage():
    members = User.query.filter_by(team_id=current_user.team_id)\
                        .order_by(User.role.desc(), User.username).all()
    return render_template('team/manage.html', members=members, team=current_user.team)


@team_bp.route('/regenerate-code', methods=['POST'])
@login_required
@admin_required
def regenerate_code():
    current_user.team.regenerate_invite_code()
    db.session.commit()
    flash('Codice invito rigenerato con successo.', 'success')
    return redirect(url_for('team.manage'))


@team_bp.route('/remove/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def remove_member(user_id):
    user = User.query.get_or_404(user_id)
    if user.team_id != current_user.team_id:
        abort(403)
    if user.id == current_user.id:
        flash('Non puoi rimuovere te stesso.', 'danger')
        return redirect(url_for('team.manage'))
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'{username} rimosso dal team.', 'success')
    return redirect(url_for('team.manage'))


@team_bp.route('/promote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def promote_member(user_id):
    user = User.query.get_or_404(user_id)
    if user.team_id != current_user.team_id:
        abort(403)
    if user.id == current_user.id:
        flash('Non puoi modificare il tuo stesso ruolo.', 'danger')
        return redirect(url_for('team.manage'))
    user.role = 'admin' if user.role == 'member' else 'member'
    db.session.commit()
    flash(f'Ruolo di {user.username} aggiornato a {user.role}.', 'success')
    return redirect(url_for('team.manage'))
