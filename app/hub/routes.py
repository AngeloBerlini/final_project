from flask import render_template, request
from flask_login import login_required, current_user
from app.models import Post, Setup, Strategy, Circuit
from app.hub import hub_bp


@hub_bp.route('/')
@login_required
def index():
    circuit_id = request.args.get('circuit_id', type=int)
    team_id = current_user.team_id

    posts_q = Post.query.filter_by(team_id=team_id)
    setups_q = Setup.query.filter_by(team_id=team_id)
    strategies_q = Strategy.query.filter_by(team_id=team_id)

    if circuit_id:
        posts_q = posts_q.filter_by(circuit_id=circuit_id)
        setups_q = setups_q.filter_by(circuit_id=circuit_id)
        strategies_q = strategies_q.filter_by(circuit_id=circuit_id)

    items = []
    for p in posts_q.all():
        items.append({'type': 'post', 'obj': p, 'date': p.created_at})
    for s in setups_q.all():
        items.append({'type': 'setup', 'obj': s, 'date': s.created_at})
    for st in strategies_q.all():
        items.append({'type': 'strategy', 'obj': st, 'date': st.created_at})

    items.sort(key=lambda x: x['date'], reverse=True)

    circuits = Circuit.query.order_by(Circuit.name).all()
    return render_template('hub/index.html', items=items, circuits=circuits,
                           selected_circuit=circuit_id)
