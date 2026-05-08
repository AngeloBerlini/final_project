import secrets
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    invite_code = db.Column(db.String(32), unique=True, nullable=False,
                            default=lambda: secrets.token_hex(8))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship('User', backref='team', lazy='dynamic')
    posts = db.relationship('Post', backref='team', lazy='dynamic')

    def regenerate_invite_code(self):
        self.invite_code = secrets.token_hex(8)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='member')
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic',
                            foreign_keys='Post.author_id')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    uploaded_media = db.relationship('Media', backref='uploader', lazy='dynamic',
                                     foreign_keys='Media.uploaded_by')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'


class Circuit(db.Model):
    __tablename__ = 'circuit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    length_km = db.Column(db.Float, nullable=False)
    num_curves = db.Column(db.Integer, nullable=False)
    lap_record = db.Column(db.String(50))
    layout_image = db.Column(db.String(200))

    posts = db.relationship('Post', backref='circuit', lazy='dynamic')


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    circuit_id = db.Column(db.Integer, db.ForeignKey('circuit.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', backref='post', lazy='dynamic',
                               cascade='all, delete-orphan')
    media_files = db.relationship('Media', backref='post', lazy='dynamic',
                                  cascade='all, delete-orphan')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    original_name = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


TIRE_COMPOUNDS = ['morbide', 'medie', 'dure', 'intermedie', 'da bagnato']


class Setup(db.Model):
    __tablename__ = 'setup'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    circuit_id = db.Column(db.Integer, db.ForeignKey('circuit.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Aerodynamica
    ala_anteriore = db.Column(db.Float)       # mm
    ala_posteriore = db.Column(db.Float)      # mm
    # Differenziale
    differenziale = db.Column(db.Float)       # %
    # Geometria sospensioni
    camber_ant = db.Column(db.Float)          # gradi
    camber_post = db.Column(db.Float)         # gradi
    toe_ant = db.Column(db.Float)             # mm
    toe_post = db.Column(db.Float)            # mm
    # Sospensioni (stiffness / click)
    sospensioni_ant = db.Column(db.String(50))
    sospensioni_post = db.Column(db.String(50))
    # Freni
    bilanciamento_freni = db.Column(db.Integer)  # %
    # Pressioni pneumatici (psi)
    pressione_ant_sx = db.Column(db.Float)
    pressione_ant_dx = db.Column(db.Float)
    pressione_post_sx = db.Column(db.Float)
    pressione_post_dx = db.Column(db.Float)
    # Note libere
    note = db.Column(db.Text)

    circuit = db.relationship('Circuit', backref=db.backref('setups', lazy='dynamic'))
    team_rel = db.relationship('Team', foreign_keys=[team_id],
                               backref=db.backref('setups', lazy='dynamic'))
    author = db.relationship('User', foreign_keys=[author_id],
                             backref=db.backref('setups', lazy='dynamic'))


class Strategy(db.Model):
    __tablename__ = 'strategy'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    circuit_id = db.Column(db.Integer, db.ForeignKey('circuit.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    circuit = db.relationship('Circuit', backref=db.backref('strategies', lazy='dynamic'))
    team_rel = db.relationship('Team', foreign_keys=[team_id],
                               backref=db.backref('strategies', lazy='dynamic'))
    author = db.relationship('User', foreign_keys=[author_id],
                             backref=db.backref('strategies', lazy='dynamic'))
    stints = db.relationship('StrategyStint', backref='strategy', lazy='dynamic',
                             cascade='all, delete-orphan',
                             order_by='StrategyStint.position')


class StrategyStint(db.Model):
    __tablename__ = 'strategy_stint'
    id = db.Column(db.Integer, primary_key=True)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    tire_compound = db.Column(db.String(20), nullable=False)
    laps = db.Column(db.Integer, nullable=False)
