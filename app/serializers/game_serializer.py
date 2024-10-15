from marshmallow import Schema, fields

class GameSchema(Schema):
  id = fields.Int()
  turn_number = fields.Int()
  turn_color = fields.Str()
  previous_fen = fields.Str()
  current_fen = fields.Str()
  white_player_id = fields.Int()
  black_player_id = fields.Int()
  white_player_points = fields.Int()
  black_player_points = fields.Int()
  game_complete = fields.Bool()
  game_outcome = fields.Str()
  game_champion = fields.Str()
  last_move = fields.Str()