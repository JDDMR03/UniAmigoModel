from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import jwt
import datetime
import requests
from functools import wraps

app = Flask(__name__)

# Configure the SQLAlchemy connection to MariaDB using environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST', 'localhost')
SECRET_KEY = os.getenv('SECRET_KEY')
MASTER_TOKEN = os.getenv('MASTER_TOKEN')

if not all([db_user, db_password, db_name, SECRET_KEY, MASTER_TOKEN]):
    raise ValueError("Missing required environment variables")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Define the UnhandledMessage model
class UnhandledMessage(db.Model):
    __tablename__ = 'unhandled_messages'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('messages', lazy=True))

def encode_auth_token(user_id):
    """Generate an authentication token."""
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return str(e)

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

# Decorator to protect routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing!'}), 403
        
        try:
            token = auth_header.split(" ")[1]
            user_id = decode_auth_token(token)
            if isinstance(user_id, str):
                return jsonify({'message': user_id}), 403
        except IndexError:
            return jsonify({'message': 'Invalid token header. Token should be provided as: Bearer <token>'}), 403

        return f(user_id, *args, **kwargs)
    return decorated

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    master_token = request.headers.get('Authorization')

    if not master_token or master_token != f'Bearer {MASTER_TOKEN}':
        return jsonify({'message': 'Unauthorized'}), 403

    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    
    if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Za-z]', password):
        return jsonify({'message': 'Password must be at least 8 characters long and contain both letters and numbers'}), 400

    new_user = User(username=username, is_admin=is_admin)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    master_token = request.headers.get('Authorization')

    if not master_token or master_token != f'Bearer {MASTER_TOKEN}':
        return jsonify({'message': 'Unauthorized'}), 403

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = encode_auth_token(user.id)
        return jsonify({'message': 'Login successful', 'token': token}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {user.username} deleted'}), 200

@app.route('/api/model/send', methods=['POST'])
@token_required
def send_message_to_model(user_id):
    data = request.json
    sender = data.get('sender')
    message = data.get('message')

    if not sender or not message:
        return jsonify({'message': 'Sender and message are required'}), 400

    payload = {
        'sender': sender,
        'message': message
    }

    try:
        response = requests.post(
            'http://model.uniamigomodel.com/webhooks/rest/webhook',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'message': f'Failed to send message: {str(e)}'}), 500

    return jsonify(response.json()), response.status_code

@app.route('/api/messages', methods=['POST'])
@token_required
def create_message(user_id):
    data = request.json
    if 'user_id' not in data or 'message_text' not in data:
        return jsonify({'message': 'User ID and message text are required'}), 400
    new_message = UnhandledMessage(user_id=data['user_id'], message_text=data['message_text'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message created'}), 201

@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
@token_required
def delete_message(message_id):
    message = UnhandledMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': f'Message {message_id} deleted'}), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    })

@app.route('/api/users/username/<string:username>', methods=['GET'])
@token_required
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify({
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    })

@app.route('/api/users', methods=['GET'])
@token_required
def get_all_users(user_id):
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    } for user in users])

@app.route('/api/messages/<int:message_id>', methods=['GET'])
@token_required
def get_message(message_id):
    message = UnhandledMessage.query.get_or_404(message_id)
    return jsonify({
        'message_id': message.message_id,
        'user_id': message.user_id,
        'message_text': message.message_text,
        'created_at': message.created_at
    })

@app.route('/api/messages', methods=['GET'])
@token_required
def get_all_messages(user_id):
    messages = UnhandledMessage.query.all()
    return jsonify([{
        'message_id': message.message_id,
        'user_id': message.user_id,
        'message_text': message.message_text,
        'created_at': message.created_at
    } for message in messages])

@app.route('/api/messages/user/<int:user_id>', methods=['GET'])
@token_required
def get_messages_by_user(user_id):
    messages = UnhandledMessage.query.filter_by(user_id=user_id).all()
    if not messages:
        return jsonify({'message': 'No messages found for this user'}), 404
    return jsonify([{
        'message_id': message.message_id,
        'user_id': message.user_id,
        'message_text': message.message_text,
        'created_at': message.created_at
    } for message in messages])

if __name__ == '__main__':
    app.run(debug=True)
