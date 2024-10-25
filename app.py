import requests
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send, rooms, join_room, leave_room, close_room, disconnect
from flask_cors import CORS


# Initialize the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# SQLite Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess_game.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize extensions
socketio = SocketIO(app, cors_allowed_origins="*")
db = SQLAlchemy(app)

# Define the Game model for SQLite, add more columns if needed (FEN, etc.)
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


# Create the database tables (for development, remove in production)
with app.app_context():
    db.create_all()


# Helper function to emit the latest game data
def emit_latest(game):
    if game is None:
        return  # Handle missing game in the caller
    
    game_data = {
        'game_id': game.id,
        'white_player_id': game.white_player_id,
        'black_player_id': game.black_player_id,
        'turn_number': game.turn_number,
        'turn_color': game.turn_color,
        'current_fen': game.current_fen,
        'previous_fen': game.previous_fen,
        'white_player_points': game.white_player_points,
        'black_player_points': game.black_player_points,
        'white_player_user_name': game.white_player_user_name,
        'black_player_user_name': game.black_player_user_name,
        'game_complete': game.game_complete,
        'game_outcome': game.game_outcome,
        'game_champion': game.game_champion
    }
    
    emit('latest', game_data, room=str(game.id))


# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    game_id = request.args.get('gameId')
    if not game_id:
        print('No game id provided.')
        emit('error', {'message': 'Connection request must contain game id.'})
        return
    
    game = Game.query.get(game_id)
    join_room(str(game_id))
    
    if not game:
        print(f'No game found for id {game_id}')
        emit('error', {'message': 'Game not found'})
        return
    
    emit_latest(game)


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print(f'Client {sid} disconnected')
    
    # Get all the rooms the client is in
    client_rooms = rooms(sid=sid)
    for room in client_rooms:
        if room != sid:  # Avoid processing the client's personal room (SID room)
            leave_room(room)
            # Check if the room has no other participants
            if not socketio.server.manager.rooms['/'].get(room):
                close_room(room)
                print(f'Room {room} is empty and has been closed')
    disconnect()


@socketio.on('make_move')
def handle_move(data):
    game_id = data['game_id']
    fen = data['current_fen']

    game = Game.query.get(game_id)
    if not game:
        emit('error', {'message': 'Game not found'})
        return

    # Check if the FEN is different from the current one
    if game.current_fen != fen:
        game.turn_number += 1
        game.previous_fen = game.current_fen
        game.current_fen = fen
        
        # Update the turn color based on the FEN string
        game.turn_color = 'white' if 'w' in fen else 'black'

    # Regardless of FEN change, commit any changes and emit the latest game state
    db.session.commit()
    emit_latest(game)  # This will emit the updated state, including white/black usernames


@socketio.on('end_game')
def handle_end_game(data):
    game_id = data['game_id']
    current_fen = data['current_fen']
    game_outcome = data['game_outcome']
    game_champion = data['game_champion']

    game = Game.query.get(game_id)
    if not game:
        emit('error', {'message': 'Game not found'})
        return

    game.previous_fen = game.current_fen
    game.current_fen = current_fen
    game.game_champion = game_champion
    game.game_outcome = game_outcome
    game.game_complete = True
    db.session.commit()
    emit_latest(game)


# API routes
@app.route('/games/<game_id>', methods=['GET'])
def get_game_state(game_id):
    print('Handling get game state event')
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'message': 'Game not found'}), 404

    return jsonify({
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
    })

@app.route('/api/v1/new_game', methods=['POST'])
def new_game():
    data = request.json

    # Handle missing JSON body
    if not data:
        return jsonify({'message': 'No JSON body provided'}), 400

    white_player_id = data.get('white_player_id')
    black_player_id = data.get('black_player_id')
    white_player_user_name = data.get('white_player_user_name')
    black_player_user_name = data.get('black_player_user_name')

    new_game = Game(
        turn_number=1,
        turn_color='white',
        previous_fen=None,
        current_fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        white_player_id=white_player_id,
        black_player_id=black_player_id,
        white_player_user_name=white_player_user_name,
        black_player_user_name=black_player_user_name,
        white_player_points=0,
        black_player_points=0,
        game_complete=False
    )

    db.session.add(new_game)
    db.session.commit()
    
    return jsonify(
        {
            'message': 'New game created',
            'game': {
                'id': new_game.id,
                'type': 'game_information',
                'attributes': {
                    'turn_number': new_game.turn_number,
                    'turn_color': new_game.turn_color,
                    'white_player_id': new_game.white_player_id,
                    'black_player_id': new_game.black_player_id,
                    'white_player_user_name': new_game.white_player_user_name,
                    'black_player_user_name': new_game.black_player_user_name,
                    'white_player_points': new_game.white_player_points,
                    'black_player_points': new_game.black_player_points,
                    'game_complete': new_game.game_complete,
                    # Include any additional game state information
                    'game_outcome': new_game.game_outcome,
                    'game_champion': new_game.game_champion
                }
            }
        }
    ), 201

# Function to send game data to the Rails backend (request to Rails backend)
def send_game_data_to_backend(game_data):
    url = "https://chess-with-frein-emies-e45d9fb62d80.herokuapp.com/api/v1/games"  # Production API, change to local host for development 
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=game_data, headers=headers)
        if response.status_code != 200:
            print(f"Error sending data to backend: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to backend: {e}")


# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', 'localhost')
    socketio.run(app, host=host, port=port, debug=True)

