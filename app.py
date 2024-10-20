from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send 
from flask_cors import CORS
import requests

# Initialize the Flask app
app = Flask(__name__)
CORS(app)


# SQLite Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess_game.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize extensions
socketio = SocketIO(app, cors_allowed_origins="*")
db = SQLAlchemy(app)

# Define the Game model for SQLite, add more columns if needed FEN etc.
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turn_number = db.Column(db.Integer, nullable=False)
    turn_color = db.Column(db.String(10), nullable=False)
    previous_fen = db.Column(db.String(100), nullable=True)
    current_fen = db.Column(db.String(100), nullable=False)
    white_player_id = db.Column(db.Integer, nullable=False)
    black_player_id = db.Column(db.Integer, nullable=False)
    white_player_user_name = db.Column(db.String(50), nullable=False)
    black_player_user_name = db.Column(db.String(50), nullable=False)
    white_player_points = db.Column(db.Integer, nullable=False)
    black_player_points = db.Column(db.Integer, nullable=False)
    game_complete = db.Column(db.Boolean, default=False)
    game_outcome = db.Column(db.String(50), nullable=True)
    game_champion = db.Column(db.String(50), nullable=True)

# Create the database tables (this is for development, remove in production)
with app.app_context():
    db.create_all()

# WebSocket handler for starting a new game
@socketio.on('start_game')
def handle_start_game(data):
    game = Game(
        turn_number=1,
        turn_color='white',
        previous_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 
        current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        white_player_id=data['white_player_id'],
        black_player_id=data['black_player_id'],
        white_player_user_name=data['white_player_user_name'],
        black_player_user_name=data['black_player_user_name'],
        white_player_points=0,
        black_player_points=0,
        game_complete=False
    )
    db.session.add(game)
    db.session.commit()

    game_data = {
        'game_id': game.id,
        'turn_number': game.turn_number,
        'turn_color': game.turn_color,
        'current_fen': game.current_fen,
        'previous_fen': game.previous_fen
    }
    
    emit('game_started', game_data, broadcast=True)

# WebSocket handler for making a move
@socketio.on('make_move')
def handle_move(data):
    game_id = data['game_id']
    fen = data['fen']  # Receive FEN from the front-end move

    game = Game.query.get(game_id)
    if not game:
        emit('error', {'message': 'Game not found'})
        return

    game.turn_number += 1
    game.previous_fen = game.current_fen
    game.current_fen = fen  # Update current FEN from the move
    game.turn_color = 'black' if game.turn_color == 'white' else 'white'
    db.session.commit()

    game_data = {
        'game_id': game.id,
        'turn_number': game.turn_number,
        'turn_color': game.turn_color,
        'current_fen': game.current_fen,
        'previous_fen': game.previous_fen,
        'white_player_points': game.white_player_points,
        'black_player_points': game.black_player_points,
        'game_complete': game.game_complete,
        'game_outcome': game.game_outcome,
        'game_champion': game.game_champion
    }

    emit('move_made', game_data, broadcast=True)
    send_game_data_to_backend(game_data)  # Send game data to Rails API

def send_latest(socket):
        game_data = {
        'game_id': game.id,
        'turn_number': game.turn_number,
        'turn_color': game.turn_color,
        'current_fen': game.current_fen,
        'previous_fen': game.previous_fen
    }
        socket.emit('latest', game_data)


# Function to send game data to the Rails backend (request to rails backend)
def send_game_data_to_backend(game_data):
    url = "https://chess-with-frein-emies-e45d9fb62d80.herokuapp.com/api/v1/games"  # Production API, change to local host for development 
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=game_data, headers=headers)
        if response.status_code != 200:
            print(f"Error sending data to backend: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to backend: {e}")

@app.route('/games/<game_id>', methods=['GET'])
def get_game_state(game_id):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'message': 'Game not found'}), 404

    return jsonify(
        {
            "data": {
            "id": game.id,
            "type": 'game_information',
            "attributes": {
                'turn_number': game.turn_number,
                'turn_color': game.turn_color,
                'white_player_id': game.white_player_id,
                'black_player_id': game.black_player_id,
                'white_player_user_name': game.white_player_user_name,
                'black_player_user_name': game.black_player_user_name,
                'white_player_points': game.white_player_points,
                'black_player_points': game.black_player_points,
                'game_complete': game.game_complete,
                'game_outcome': game.game_outcome,
                'game_champion': game.game_champion
            }
        }
    }
)

# Run the Flask app
if __name__ == '__main__':
    socketio.run(app)      #change parameters to use debug=True when testing (app, debug=True)
