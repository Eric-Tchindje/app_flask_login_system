from flask import Flask, render_template, request, redirect, url_for, session
from accounts.views import accounts
from db_extensions import db
from flask_migrate import Migrate
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # Initialize SQLAlchemy and Migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(accounts)

    @app.route('/')
    def home():
        if 'loggedin' in session:
            return render_template('index.html', username=session['username'])
        return redirect(url_for('accounts.login'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app


# Gunicorn will use this
app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
