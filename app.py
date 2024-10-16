from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import requests

# Initialize the Flask app
app = Flask(__name__)

# SQLite Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess_game.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
socketio = SocketIO(app)
db = SQLAlchemy(app)

# Define the Game model for SQLite, add more columns if needed FEN etc.
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turn_number = db.Column(db.Integer, nullable=False)
    turn_color = db.Column(db.String(10), nullable=False)
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
    # Need to confer with front end team on what data to send
    game_data = {
        'game_id': game.id,
        'turn_number': game.turn_number,
        'turn_color': game.turn_color
    }
    
    emit('game_started', game_data, broadcast=True)

# WebSocket handler for making a move
@socketio.on('make_move')
def handle_move(data):
    game_id = data['game_id']
    move = data['move']

    game = Game.query.get(game_id)
    if not game:
        emit('error', {'message': 'Game not found'})
        return

    game.turn_number += 1
    game.turn_color = 'black' if game.turn_color == 'white' else 'white'
    db.session.commit()

    emit('move_made', data, broadcast=True)
    send_game_data_to_backend({
        'game_id': game.id,
        'turn_number': game.turn_number,
        'turn_color': game.turn_color,
        'white_player_points': game.white_player_points,
        'black_player_points': game.black_player_points,
        'game_complete': game.game_complete
    })

# Function to send game data to the Rails backend
def send_game_data_to_backend(game_data):
    url = "http://localhost:3000/api/v1/games"  # Local Rails API URL
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=game_data, headers=headers)
    return response.status_code

# Run the Flask app
if __name__ == '__main__':
    socketio.run(app, debug=True)
