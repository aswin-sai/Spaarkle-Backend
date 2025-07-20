from flask import Flask
from config import Config
from extensions import db, mail, jwt, cors
from routes.public_routes import public_bp
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.upload_routes import upload_bp
from flask import send_from_directory
import os

# NOTE:
# If you get "ImportError: DLL load failed while importing _psycopg" on Windows,
# uninstall psycopg2 and install psycopg2-binary instead:
#   pip uninstall psycopg2
#   pip install psycopg2-binary
# This resolves most DLL issues on Windows environments.

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Register admin routes BEFORE public routes to avoid shadowing
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(upload_bp, url_prefix='/upload')

    # Serve uploaded files
    @app.route('/static/uploads/<path:filename>')
    def uploaded_file(filename):
        upload_dir = os.path.join(app.root_path, 'static', 'uploads')
        return send_from_directory(upload_dir, filename)

    # Add root route for Render
    @app.route('/')
    def index():
        return 'Welcome to the Event Manager API!'
    return app

if __name__ == "__main__":
    app = create_app()
    # --- TEMPORARY: Create all tables if they do not exist ---
    from extensions import db
    with app.app_context():
        db.create_all()
        # --- TEMPORARY: Create admin user a@a.com with password 'a' ---
        from models import AdminUser
        from utils.auth import hash_password
        if not AdminUser.query.filter_by(email="a@a.com").first():
            user = AdminUser(email="a@a.com", hashed_password=hash_password("a"))
            db.session.add(user)
            db.session.commit()
        # --- Remove the above after the user is created ---
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
