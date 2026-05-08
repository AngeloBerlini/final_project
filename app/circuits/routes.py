import os
from flask import render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from app import db
from app.models import Circuit
from app.circuits import circuits_bp

ALLOWED_IMAGE_EXT = {'png', 'jpg', 'jpeg', 'webp', 'svg'}


@circuits_bp.route('/')
def list():
    circuits = Circuit.query.order_by(Circuit.country, Circuit.name).all()
    return render_template('circuits/list.html', circuits=circuits)


@circuits_bp.route('/<int:circuit_id>')
def detail(circuit_id):
    circuit = Circuit.query.get_or_404(circuit_id)
    return render_template('circuits/detail.html', circuit=circuit)


@circuits_bp.route('/<int:circuit_id>/upload-image', methods=['POST'])
@login_required
def upload_image(circuit_id):
    if not current_user.is_admin():
        abort(403)
    circuit = Circuit.query.get_or_404(circuit_id)
    f = request.files.get('layout_image')
    if not f or not f.filename:
        flash('Nessun file selezionato.', 'warning')
        return redirect(url_for('circuits.detail', circuit_id=circuit_id))
    ext = f.filename.rsplit('.', 1)[-1].lower() if '.' in f.filename else ''
    if ext not in ALLOWED_IMAGE_EXT:
        flash('Formato non supportato. Usa PNG, JPG, WebP o SVG.', 'danger')
        return redirect(url_for('circuits.detail', circuit_id=circuit_id))
    static_dir = os.path.join(current_app.root_path, 'static', 'circuits')
    os.makedirs(static_dir, exist_ok=True)
    filename = f'circuit_{circuit_id}.{ext}'
    f.save(os.path.join(static_dir, filename))
    circuit.layout_image = f'circuits/{filename}'
    db.session.commit()
    flash('Layout del circuito caricato.', 'success')
    return redirect(url_for('circuits.detail', circuit_id=circuit_id))
