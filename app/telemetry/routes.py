from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Telemetry, Setup, Circuit
from app.telemetry import telemetry_bp
from app.telemetry.utils import generate_telemetry_charts, generate_pedal_charts
import json


@telemetry_bp.route('/upload/<int:setup_id>', methods=['GET', 'POST'])
@login_required
def upload_telemetry(setup_id):
    """Carica dati di telemetria per un setup."""
    setup = Setup.query.get_or_404(setup_id)
    
    # Verifica che l'utente appartenga al team
    if setup.team_id != current_user.team_id:
        flash('Non hai permesso di accedere a questo setup.', 'danger')
        return redirect(url_for('posts.list'))
    
    if request.method == 'POST':
        try:
            # Ricevi i dati telemetrici come JSON
            dati = request.get_json() or request.form
            
            telemetry = Telemetry(
                setup_id=setup_id,
                circuit_id=setup.circuit_id,
                team_id=current_user.team_id,
                author_id=current_user.id,
                velocita=json.loads(dati.get('velocita', '[]')) if isinstance(dati.get('velocita'), str) else dati.get('velocita'),
                rpm=json.loads(dati.get('rpm', '[]')) if isinstance(dati.get('rpm'), str) else dati.get('rpm'),
                temperatura_freni=json.loads(dati.get('temperatura_freni', '[]')) if isinstance(dati.get('temperatura_freni'), str) else dati.get('temperatura_freni'),
                temperatura_gomme=json.loads(dati.get('temperatura_gomme', '[]')) if isinstance(dati.get('temperatura_gomme'), str) else dati.get('temperatura_gomme'),
                accelerazione=json.loads(dati.get('accelerazione', '[]')) if isinstance(dati.get('accelerazione'), str) else dati.get('accelerazione'),
                gas=json.loads(dati.get('gas', '[]')) if isinstance(dati.get('gas'), str) else dati.get('gas'),
                freno=json.loads(dati.get('freno', '[]')) if isinstance(dati.get('freno'), str) else dati.get('freno'),
                sterzo=json.loads(dati.get('sterzo', '[]')) if isinstance(dati.get('sterzo'), str) else dati.get('sterzo'),
                descrizione=dati.get('descrizione', '')
            )
            
            db.session.add(telemetry)
            db.session.flush()
            
            # Genera i grafici
            charts_info = generate_telemetry_charts(telemetry, current_app.config['UPLOAD_FOLDER'])
            charts_info.update(generate_pedal_charts(telemetry, current_app.config['UPLOAD_FOLDER']))
            
            db.session.commit()
            flash('Dati telemetrici caricati con successo!', 'success')
            return redirect(url_for('telemetry.view_telemetry', telemetry_id=telemetry.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Errore nel caricamento dei dati: {str(e)}', 'danger')
    
    return render_template('telemetry/upload.html', setup=setup)


@telemetry_bp.route('/view/<int:telemetry_id>')
@login_required
def view_telemetry(telemetry_id):
    """Visualizza i dati e i grafici di telemetria."""
    telemetry = Telemetry.query.get_or_404(telemetry_id)
    
    # Verifica che l'utente appartenga al team
    if telemetry.team_id != current_user.team_id:
        flash('Non hai permesso di accedere a questi dati.', 'danger')
        return redirect(url_for('posts.list'))
    
    return render_template('telemetry/view.html', telemetry=telemetry)


@telemetry_bp.route('/list/<int:setup_id>')
@login_required
def list_telemetry(setup_id):
    """Elenca tutti i dati telemetrici di un setup."""
    setup = Setup.query.get_or_404(setup_id)
    
    # Verifica che l'utente appartenga al team
    if setup.team_id != current_user.team_id:
        flash('Non hai permesso di accedere a questo setup.', 'danger')
        return redirect(url_for('posts.list'))
    
    telemetry_records = Telemetry.query.filter_by(setup_id=setup_id).order_by(Telemetry.created_at.desc()).all()
    
    return render_template('telemetry/list.html', setup=setup, telemetry_records=telemetry_records)


@telemetry_bp.route('/delete/<int:telemetry_id>', methods=['POST'])
@login_required
def delete_telemetry(telemetry_id):
    """Elimina un record di telemetria."""
    telemetry = Telemetry.query.get_or_404(telemetry_id)
    
    # Verifica che sia admin o autore
    if telemetry.author_id != current_user.id and not current_user.is_admin():
        flash('Non hai permesso di eliminare questo record.', 'danger')
        return redirect(url_for('posts.list'))
    
    setup_id = telemetry.setup_id
    db.session.delete(telemetry)
    db.session.commit()
    
    flash('Record telemetrico eliminato.', 'success')
    return redirect(url_for('telemetry.list_telemetry', setup_id=setup_id))
