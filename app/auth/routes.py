from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User, Team
from app.auth import auth_bp


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.list'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        action = request.form.get('action', 'join')

        if not username or not email or not password:
            flash('Compila tutti i campi obbligatori.', 'danger')
            return render_template('auth/register.html')
        if User.query.filter_by(email=email).first():
            flash('Email già registrata.', 'danger')
            return render_template('auth/register.html')
        if User.query.filter_by(username=username).first():
            flash('Username già in uso.', 'danger')
            return render_template('auth/register.html')

        if action == 'create':
            team_name = request.form.get('team_name', '').strip()
            if not team_name:
                flash('Inserisci il nome del team.', 'danger')
                return render_template('auth/register.html')
            if Team.query.filter_by(name=team_name).first():
                flash('Nome team già in uso.', 'danger')
                return render_template('auth/register.html')
            team = Team(name=team_name)
            db.session.add(team)
            db.session.flush()
            user = User(username=username, email=email, team_id=team.id, role='admin')
        else:
            invite_code = request.form.get('invite_code', '').strip()
            team = Team.query.filter_by(invite_code=invite_code).first()
            if not team:
                flash('Codice invito non valido.', 'danger')
                return render_template('auth/register.html')
            user = User(username=username, email=email, team_id=team.id, role='member')

        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Benvenuto in {team.name}!', 'success')
        return redirect(url_for('posts.list'))
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.list'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('hub.index'))
        flash('Credenziali non valide.', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
