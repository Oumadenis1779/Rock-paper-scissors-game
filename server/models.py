from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    score = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def register_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

def check_user_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return True
    return False

def update_score(username, result):
    user = User.query.filter_by(username=username).first()
    if user:
        if result == "win":
            user.score += 1
        elif result == "lose":
            user.score -= 1
        db.session.commit()

def get_user_score(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.score
    return None

# Game logic remains the same
def play_game(player_choice):
    return