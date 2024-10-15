import os

# stores all configurations like the database URI and secret key.
class Config:
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://username:password@localhost/mydatabase')