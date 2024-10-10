from flask import Flask, request, jsonify 

app = Flask(__name__)

@app.route("/")
def home():
  return "Home"

@app.route("/games/<game_id>")
def get_game(game_id):
  game_data = {
    "data": {
      "id": game_id,
      "type": "game_state",
      "attributes": {
        "turn_number": "2",
        "turn_color": "black",
        "previous_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "current_fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        "white_player_id": "1",
        "black_player_id": "2",
        "white_player_points": "0",
        "black_player_points": "0",
        "game_complete": "false",
        "game_outcome": "null",
        "game_champion": "null",
        "last_move": ""
      }
    }
  }

  return jsonify(game_data), 200

@app.route("/game/new", methods=["POST"])
def create_game():
  data = request.get_json() #getting json from body of users request

  return jsonify(data), 201


if __name__ == "__main__":
  app.run(debug=True)