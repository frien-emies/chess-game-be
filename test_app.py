import unittest
from app import app, db, socketio, Game
from flask_socketio import SocketIOTestClient

class ChessGameTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()
            self.init_mock_game()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def init_mock_game(self):
        game = Game(
            id=1,
            turn_number=1,
            turn_color='white',
            current_fen="initial_fen_string",
            white_player_id=1,
            black_player_id=2,
            white_player_user_name="Player1",
            black_player_user_name="Player2",
            white_player_points=0,
            black_player_points=0
        )
        db.session.add(game)
        db.session.commit()

    def test_get_game_state(self):
        response = self.app.get('/api/v1/games/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('data', data)
        self.assertEqual(data['data']['id'], 1)
        self.assertEqual(data['data']['attributes']['turn_color'], 'white')

    def test_get_game_state_not_found(self):
        response = self.app.get('/api/v1/games/999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['message'], 'Game not found')
    
    def test_new_game_creation(self):
        # payload to create a new game
        payload = {
            'white_player_id': 1,
            'black_player_id': 2,
            'white_player_user_name': 'Player1',
            'black_player_user_name': 'Player2'
        }

        response = self.app.post('/api/v1/new_game', json=payload)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'New game created')
        self.assertIn('game', data)
        self.assertEqual(data['game']['attributes']['turn_number'], 1)
        self.assertEqual(data['game']['attributes']['turn_color'], 'white')
        self.assertEqual(data['game']['attributes']['white_player_id'], 1)
        self.assertEqual(data['game']['attributes']['black_player_id'], 2)
    
    def test_no_json_body(self):
        response = self.app.post('/api/v1/new_game')

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], 'No JSON body provided')

def test_socket_connect_and_make_move(self):
    # Create SocketIO test client linked to socketio instance
    socketio_client = socketio.test_client(app, query_string={'gameId': '1'})  # Pass gameId in query_string

    # Now check the received messages after connecting
    received = socketio_client.get_received()
    print(f"Received after connect: {received}")  # Debugging

    # Ensure game was found and connection was successful
    self.assertNotIn('error', [r['name'] for r in received], "Game should be found")
    self.assertIn('latest', [r['name'] for r in received])

    # Make a move and check updates
    socketio_client.emit('make_move', {'game_id': 1, 'current_fen': 'updated_fen_string'})
    received = socketio_client.get_received()
    print(f"Received after make_move: {received}")  # Debugging
    self.assertIn('latest', [r['name'] for r in received])
    self.assertEqual(received[0]['args'][0]['current_fen'], 'updated_fen_string')

if __name__ == "__main__":
    unittest.main()

