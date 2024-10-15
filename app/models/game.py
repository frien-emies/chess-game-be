from app import db

# defines the database schema for the game.

class Game(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  turn_number = db.Column(db.Integer, nullable=False)
  turn_color = db.Column(db.String(20), nullable=False)
  previous_fen = db.Column(db.String(200), nullable=False)
  current_fen = db.Column(db.String(200), nullable=False)
  white_player_id = db.Column(db.Integer, nullable=False)
  black_player_id = db.Column(db.Integer, nullable=False)
  white_player_points = db.Column(db.Integer, default=0)
  black_player_points = db.Column(db.Integer, default=0)
  game_complete = db.Column(db.Boolean, default=False)
  game_outcome = db.Column(db.String(100), nullable=True)
  game_champion = db.Column(db.String(100), nullable=True)
  last_move = db.Column(db.String(100), nullable=True)

  def __repr__(self):
    return f"<Game {self.id} - Turn {self.turn_number}>"