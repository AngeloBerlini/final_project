from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Strategy, StrategyStint, Circuit, TIRE_COMPOUNDS
from app.strategy import strategy_bp


def _parse_stints(form):
    stints = []
    i = 1
    while True:
        tire = form.get(f'tire_{i}')
        if tire is None:
            break
        laps_raw = form.get(f'laps_{i}', '').strip()
        try:
            laps = int(laps_raw)
        except (ValueError, TypeError):
            laps = 0
        if tire in TIRE_COMPOUNDS and laps > 0:
            stints.append({'position': i, 'tire_compound': tire, 'laps': laps})
        i += 1
    return stints


@strategy_bp.route('/')
@login_required
def list():
    circuit_id = request.args.get('circuit_id', type=int)
    query = Strategy.query.filter_by(team_id=current_user.team_id)
    if circuit_id:
        query = query.filter_by(circuit_id=circuit_id)
    strategies = query.order_by(Strategy.created_at.desc()).all()
    circuits = Circuit.query.order_by(Circuit.name).all()
    return render_template('strategy/list.html', strategies=strategies, circuits=circuits,
                           selected_circuit=circuit_id)


def _circuit_laps_map(circuits):
    return {c.id: c.race_laps for c in circuits if c.race_laps}


@strategy_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    circuits = Circuit.query.order_by(Circuit.name).all()
    laps_map = _circuit_laps_map(circuits)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        circuit_id = request.form.get('circuit_id', type=int)
        note = request.form.get('note', '').strip() or None
        stints_data = _parse_stints(request.form)
        if not title or not circuit_id:
            flash('Titolo e circuito sono obbligatori.', 'danger')
            return render_template('strategy/form.html', circuits=circuits,
                                   compounds=TIRE_COMPOUNDS, laps_map=laps_map)
        if not stints_data:
            flash('Inserisci almeno uno stint valido (gomma + numero giri).', 'danger')
            return render_template('strategy/form.html', circuits=circuits,
                                   compounds=TIRE_COMPOUNDS, laps_map=laps_map)
        circuit = Circuit.query.get(circuit_id)
        if circuit and circuit.race_laps:
            total = sum(s['laps'] for s in stints_data)
            if total != circuit.race_laps:
                flash(f'Il totale degli stint ({total} giri) deve corrispondere esattamente ai giri di gara del circuito ({circuit.race_laps}).', 'danger')
                return render_template('strategy/form.html', circuits=circuits,
                                       compounds=TIRE_COMPOUNDS, laps_map=laps_map)
        strategy = Strategy(title=title, circuit_id=circuit_id,
                            team_id=current_user.team_id,
                            author_id=current_user.id, note=note)
        db.session.add(strategy)
        db.session.flush()
        for s in stints_data:
            db.session.add(StrategyStint(strategy_id=strategy.id, **s))
        db.session.commit()
        flash('Strategia salvata.', 'success')
        return redirect(url_for('strategy.detail', strategy_id=strategy.id))
    return render_template('strategy/form.html', circuits=circuits, compounds=TIRE_COMPOUNDS,
                           laps_map=laps_map)


@strategy_bp.route('/<int:strategy_id>')
@login_required
def detail(strategy_id):
    strategy = Strategy.query.get_or_404(strategy_id)
    if strategy.team_id != current_user.team_id:
        abort(403)
    stints = StrategyStint.query.filter_by(strategy_id=strategy_id)\
                                .order_by(StrategyStint.position).all()
    total_laps = sum(s.laps for s in stints)
    return render_template('strategy/detail.html', strategy=strategy,
                           stints=stints, total_laps=total_laps)


@strategy_bp.route('/<int:strategy_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(strategy_id):
    strategy = Strategy.query.get_or_404(strategy_id)
    if strategy.team_id != current_user.team_id:
        abort(403)
    if strategy.author_id != current_user.id and not current_user.is_admin():
        abort(403)
    circuits = Circuit.query.order_by(Circuit.name).all()
    laps_map = _circuit_laps_map(circuits)
    stints = StrategyStint.query.filter_by(strategy_id=strategy_id)\
                                .order_by(StrategyStint.position).all()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        circuit_id = request.form.get('circuit_id', type=int)
        note = request.form.get('note', '').strip() or None
        stints_data = _parse_stints(request.form)
        if not title or not circuit_id:
            flash('Titolo e circuito sono obbligatori.', 'danger')
            return render_template('strategy/form.html', strategy=strategy,
                                   stints=stints, circuits=circuits, compounds=TIRE_COMPOUNDS,
                                   laps_map=laps_map)
        if not stints_data:
            flash('Inserisci almeno uno stint valido.', 'danger')
            return render_template('strategy/form.html', strategy=strategy,
                                   stints=stints, circuits=circuits, compounds=TIRE_COMPOUNDS,
                                   laps_map=laps_map)
        circuit = Circuit.query.get(circuit_id)
        if circuit and circuit.race_laps:
            total = sum(s['laps'] for s in stints_data)
            if total != circuit.race_laps:
                flash(f'Il totale degli stint ({total} giri) deve corrispondere esattamente ai giri di gara del circuito ({circuit.race_laps}).', 'danger')
                return render_template('strategy/form.html', strategy=strategy,
                                       stints=stints, circuits=circuits, compounds=TIRE_COMPOUNDS,
                                       laps_map=laps_map)
        strategy.title = title
        strategy.circuit_id = circuit_id
        strategy.note = note
        StrategyStint.query.filter_by(strategy_id=strategy.id).delete()
        for s in stints_data:
            db.session.add(StrategyStint(strategy_id=strategy.id, **s))
        db.session.commit()
        flash('Strategia aggiornata.', 'success')
        return redirect(url_for('strategy.detail', strategy_id=strategy.id))
    return render_template('strategy/form.html', strategy=strategy, stints=stints,
                           circuits=circuits, compounds=TIRE_COMPOUNDS, laps_map=laps_map)


@strategy_bp.route('/<int:strategy_id>/delete', methods=['POST'])
@login_required
def delete(strategy_id):
    strategy = Strategy.query.get_or_404(strategy_id)
    if strategy.team_id != current_user.team_id:
        abort(403)
    if strategy.author_id != current_user.id and not current_user.is_admin():
        abort(403)
    db.session.delete(strategy)
    db.session.commit()
    flash('Strategia eliminata.', 'success')
    return redirect(url_for('strategy.list'))
