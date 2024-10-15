from flask import Blueprint, request, jsonify
from app.models.game import Game
from app.serializers.game_serializer import GameSchema
from app import db

# where existing routes (like getting game data and creating a new game) are
# functionality to store and retrieve games from the database as well

game_bp = Blueprint('game', __name__)

@game_bp.route("/games/<game_id>")
def get_game(game_id):
  game = Game.query.get(game_id)
  if not game:
    return jsonify({"error": "Game not found"}), 404

  game_schema = GameSchema()
  return jsonify(game_schema.dump(game)), 200

@game_bp.route("/game/new", methods=["POST"])
def create_game():
  data = request.get_json()

  new_game = Game(
      turn_number=data.get('turn_number', 1),
      turn_color=data.get('turn_color', 'white'),
      previous_fen=data.get('previous_fen', 'None'),
      current_fen=data.get('current_fen', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'),
      white_player_id=data.get('white_player_id'),
      black_player_id=data.get('black_player_id')
  )

  db.session.add(new_game)
  db.session.commit()

  game_schema = GameSchema()
  return jsonify(game_schema.dump(new_game)), 201
