# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from accounts.views import accounts
from db_extensions import db  # import db instance
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Initialize SQLAlchemy with app
db.init_app(app)

# Alembic  for the migration
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('accounts.login'))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.register_blueprint(accounts)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates all tables if they don't exist
    app.run()
