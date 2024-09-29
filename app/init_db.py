import os
from app import create_app, db
from flask_migrate import upgrade, init, migrate
import traceback
import sys

def run_migrations():
    try:
        app = create_app('development')
        with app.app_context():
            print("Creating all tables...")
            db.create_all()
            
            if not os.path.exists('migrations'):
                print("Initializing migrations...")
                init()
            
            print("Generating migration...")
            migrate(message="initial migration")
            
            print("Applying migrations...")
            upgrade()

        print("Database initialization and migration completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        print("Traceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()