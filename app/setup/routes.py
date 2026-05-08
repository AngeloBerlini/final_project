from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Setup, Circuit
from app.setup import setup_bp


def _parse_setup(form):
    def fv(key):
        v = form.get(key, '').strip()
        try:
            return float(v) if v else None
        except ValueError:
            return None

    def iv(key):
        v = form.get(key, '').strip()
        try:
            return int(v) if v else None
        except ValueError:
            return None

    return dict(
        title=form.get('title', '').strip(),
        circuit_id=iv('circuit_id'),
        ala_anteriore=fv('ala_anteriore'),
        ala_posteriore=fv('ala_posteriore'),
        differenziale=fv('differenziale'),
        camber_ant=fv('camber_ant'),
        camber_post=fv('camber_post'),
        toe_ant=fv('toe_ant'),
        toe_post=fv('toe_post'),
        sospensioni_ant=form.get('sospensioni_ant', '').strip() or None,
        sospensioni_post=form.get('sospensioni_post', '').strip() or None,
        bilanciamento_freni=iv('bilanciamento_freni'),
        pressione_ant_sx=fv('pressione_ant_sx'),
        pressione_ant_dx=fv('pressione_ant_dx'),
        pressione_post_sx=fv('pressione_post_sx'),
        pressione_post_dx=fv('pressione_post_dx'),
        note=form.get('note', '').strip() or None,
    )


@setup_bp.route('/')
@login_required
def list():
    circuit_id = request.args.get('circuit_id', type=int)
    query = Setup.query.filter_by(team_id=current_user.team_id)
    if circuit_id:
        query = query.filter_by(circuit_id=circuit_id)
    setups = query.order_by(Setup.created_at.desc()).all()
    circuits = Circuit.query.order_by(Circuit.name).all()
    return render_template('setup/list.html', setups=setups, circuits=circuits,
                           selected_circuit=circuit_id)


@setup_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    circuits = Circuit.query.order_by(Circuit.name).all()
    if request.method == 'POST':
        data = _parse_setup(request.form)
        if not data['title'] or not data['circuit_id']:
            flash('Titolo e circuito sono obbligatori.', 'danger')
            return render_template('setup/form.html', circuits=circuits)
        setup = Setup(team_id=current_user.team_id, author_id=current_user.id, **data)
        db.session.add(setup)
        db.session.commit()
        flash('Setup salvato.', 'success')
        return redirect(url_for('setup.detail', setup_id=setup.id))
    return render_template('setup/form.html', circuits=circuits)


@setup_bp.route('/<int:setup_id>')
@login_required
def detail(setup_id):
    setup = Setup.query.get_or_404(setup_id)
    if setup.team_id != current_user.team_id:
        abort(403)
    return render_template('setup/detail.html', setup=setup)


@setup_bp.route('/<int:setup_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(setup_id):
    setup = Setup.query.get_or_404(setup_id)
    if setup.team_id != current_user.team_id:
        abort(403)
    if setup.author_id != current_user.id and not current_user.is_admin():
        abort(403)
    circuits = Circuit.query.order_by(Circuit.name).all()
    if request.method == 'POST':
        data = _parse_setup(request.form)
        if not data['title'] or not data['circuit_id']:
            flash('Titolo e circuito sono obbligatori.', 'danger')
            return render_template('setup/form.html', setup=setup, circuits=circuits)
        for k, v in data.items():
            setattr(setup, k, v)
        db.session.commit()
        flash('Setup aggiornato.', 'success')
        return redirect(url_for('setup.detail', setup_id=setup.id))
    return render_template('setup/form.html', setup=setup, circuits=circuits)


@setup_bp.route('/<int:setup_id>/delete', methods=['POST'])
@login_required
def delete(setup_id):
    setup = Setup.query.get_or_404(setup_id)
    if setup.team_id != current_user.team_id:
        abort(403)
    if setup.author_id != current_user.id and not current_user.is_admin():
        abort(403)
    db.session.delete(setup)
    db.session.commit()
    flash('Setup eliminato.', 'success')
    return redirect(url_for('setup.list'))
