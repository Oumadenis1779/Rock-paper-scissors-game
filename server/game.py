from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import play_game, update_score

game_bp = Blueprint('game', __name__)

@game_bp.route('/play', methods=['POST'])
@jwt_required()
def play():
    player_choice = request.json.get('choice', None)
    result = play_game(player_choice)
    update_score(get_jwt_identity(), result)
    return jsonify(result=result), 200

