from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, register_user, check_user_credentials, play_game, update_score, get_user_score

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secrets.token_urlsafe(32)'

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username', None)
        if not username or not username.isalpha():
            return jsonify({"msg": "Invalid username. Please provide a valid username with only characters."}), 400
        
        password = request.json.get('password', None)
        register_user(username, password)
        return jsonify({"msg": "User created successfully"}), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "User not found or wrong credentials"}), 401

@app.route('/play', methods=['POST'])
@jwt_required()
def play():
    player_choice = request.json.get('choice', None)
    result = play_game(player_choice)
    update_score(get_jwt_identity(), result)
    return jsonify(result=result), 200

@app.route('/score', methods=['GET'])
@jwt_required()
def score():
    username = get_jwt_identity()
    score = get_user_score(username)
    return jsonify(score=score)

@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": f"User {username} deleted successfully"}), 200
    else:
        return jsonify({"msg": f"User {username} not found"}), 404

@app.route('/update_user/<username>', methods=['PATCH'])
def update_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        new_password = request.json.get('new_password', user.password)
        user.password = new_password
        db.session.commit()
        return jsonify({"msg": f"Password for user {username} updated successfully"}), 200
    else:
        return jsonify({"msg": f"User {username} not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)