from flask_jwt_extended import create_access_token as flask_create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed):
    return check_password_hash(hashed, password)

def create_access_token(identity):
    return flask_create_access_token(identity=identity)
