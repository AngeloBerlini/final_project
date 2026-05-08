import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Accedi per continuare.'
    login_manager.login_message_category = 'warning'

    from app.auth import auth_bp
    from app.posts import posts_bp
    from app.media import media_bp
    from app.comments import comments_bp
    from app.circuits import circuits_bp
    from app.profile import profile_bp
    from app.team import team_bp
    from app.setup import setup_bp
    from app.strategy import strategy_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(media_bp, url_prefix='/media')
    app.register_blueprint(comments_bp, url_prefix='/comments')
    app.register_blueprint(circuits_bp, url_prefix='/circuits')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(setup_bp, url_prefix='/setup')
    app.register_blueprint(strategy_bp, url_prefix='/strategy')

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('posts.list'))
        return redirect(url_for('circuits.list'))

    with app.app_context():
        db.create_all()
        _seed_circuits()

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app


def _seed_circuits():
    from app.models import Circuit
    if Circuit.query.count() > 0:
        return
    circuits = [
        Circuit(name='Bahrain International Circuit', country='Bahrain', length_km=5.412, num_curves=15, lap_record='1:31.447'),
        Circuit(name='Jeddah Corniche Circuit', country='Saudi Arabia', length_km=6.174, num_curves=27, lap_record='1:30.734'),
        Circuit(name='Albert Park Circuit', country='Australia', length_km=5.278, num_curves=16, lap_record='1:20.235'),
        Circuit(name='Suzuka International Racing Course', country='Japan', length_km=5.807, num_curves=18, lap_record='1:30.983'),
        Circuit(name='Shanghai International Circuit', country='China', length_km=5.451, num_curves=16, lap_record='1:32.238'),
        Circuit(name='Miami International Autodrome', country='USA', length_km=5.412, num_curves=19, lap_record='1:29.708'),
        Circuit(name='Autodromo Enzo e Dino Ferrari', country='Italy', length_km=4.909, num_curves=17, lap_record='1:15.484'),
        Circuit(name='Circuit de Monaco', country='Monaco', length_km=3.337, num_curves=19, lap_record='1:12.909'),
        Circuit(name='Circuit de Barcelona-Catalunya', country='Spain', length_km=4.657, num_curves=14, lap_record='1:16.330'),
        Circuit(name='Circuit Gilles Villeneuve', country='Canada', length_km=4.361, num_curves=14, lap_record='1:13.078'),
        Circuit(name='Red Bull Ring', country='Austria', length_km=4.318, num_curves=10, lap_record='1:05.619'),
        Circuit(name='Silverstone Circuit', country='United Kingdom', length_km=5.891, num_curves=18, lap_record='1:27.097'),
        Circuit(name='Hungaroring', country='Hungary', length_km=4.381, num_curves=14, lap_record='1:16.627'),
        Circuit(name='Circuit de Spa-Francorchamps', country='Belgium', length_km=7.004, num_curves=19, lap_record='1:46.286'),
        Circuit(name='Circuit Zandvoort', country='Netherlands', length_km=4.259, num_curves=14, lap_record='1:11.097'),
        Circuit(name='Autodromo Nazionale Monza', country='Italy', length_km=5.793, num_curves=11, lap_record='1:21.046'),
        Circuit(name='Baku City Circuit', country='Azerbaijan', length_km=6.003, num_curves=20, lap_record='1:43.009'),
        Circuit(name='Marina Bay Street Circuit', country='Singapore', length_km=4.940, num_curves=19, lap_record='1:35.867'),
        Circuit(name='Circuit of the Americas', country='USA', length_km=5.513, num_curves=20, lap_record='1:36.169'),
        Circuit(name='Autodromo Hermanos Rodriguez', country='Mexico', length_km=4.304, num_curves=17, lap_record='1:17.774'),
        Circuit(name='Autodromo Jose Carlos Pace', country='Brazil', length_km=4.309, num_curves=15, lap_record='1:10.540'),
        Circuit(name='Las Vegas Street Circuit', country='USA', length_km=6.201, num_curves=17, lap_record='1:35.490'),
        Circuit(name='Losail International Circuit', country='Qatar', length_km=5.380, num_curves=16, lap_record='1:24.319'),
        Circuit(name='Yas Marina Circuit', country='UAE', length_km=5.281, num_curves=16, lap_record='1:26.103'),
    ]
    db.session.bulk_save_objects(circuits)
    db.session.commit()
