from app import db, Game

def clear_data():
    db.drop_all()

# Run the seed function
if __name__ == '__main__':
    clear_data()
