from app import db, Game

# Sample data to seed the database
games = [
    {
        'turn_number': 10,
        'turn_color': 'white',
        'previous_fen': "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        'current_fen': "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        'white_player_id': 1,
        'black_player_id': 2,
        'white_player_user_name': 'Alice',
        'black_player_user_name': 'Bob',
        'white_player_points': 0,
        'black_player_points': 0,
        'game_complete': False,
        'game_outcome': None,
        'game_champion': None
    },
    {
        'turn_number': 20,
        'turn_color': 'white',
        'previous_fen': "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        'current_fen': "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        'white_player_id': 3,
        'black_player_id': 4,
        'white_player_user_name': 'Charlie',
        'black_player_user_name': 'David',
        'white_player_points': 0,
        'black_player_points': 0,
        'game_complete': True,
        'game_outcome': 'draw',
        'game_champion': None
    },
    {
        'turn_number': 5,
        'turn_color': 'white',
        'previous_fen': "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        'current_fen': "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        'white_player_id': 5,
        'black_player_id': 6,
        'white_player_user_name': 'Eve',
        'black_player_user_name': 'Frank',
        'white_player_points': 0,
        'black_player_points': 0,
        'game_complete': False,
        'game_outcome': None,
        'game_champion': None
    }
]

# Function to seed the database
def seed_games():
    for game_data in games:
        game = Game(
            turn_number=game_data['turn_number'],
            turn_color=game_data['turn_color'],
            previous_fen=game_data['previous_fen'],
            current_fen=game_data['current_fen'],
            white_player_id=game_data['white_player_id'],
            black_player_id=game_data['black_player_id'],
            white_player_user_name=game_data['white_player_user_name'],
            black_player_user_name=game_data['black_player_user_name'],
            white_player_points=game_data['white_player_points'],
            black_player_points=game_data['black_player_points'],
            game_complete=game_data['game_complete'],
            game_outcome=game_data['game_outcome'],
            game_champion=game_data['game_champion']
        )
        db.session.add(game)

    db.session.commit()
    print("Games seeded successfully!")

# Run the seed function
if __name__ == '__main__':
    seed_games()
