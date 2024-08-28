from app import create_app, db
from app.models import User
from datetime import datetime

app = create_app()  # Create an instance of your Flask app

def reset_user_dates(new_date):
    with app.app_context():  # Ensure the app context is available
        users = User.query.all()
        for user in users:
            user.date_joined = new_date
            db.session.add(user)
        db.session.commit()
        print(f"All user dates reset to {new_date}")

if __name__ == "__main__":
    # Set this to the desired reset date
    reset_date = datetime(2024, 1, 1)  # For example, January 1, 2024
    reset_user_dates(reset_date)
