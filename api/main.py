from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configure the SQLAlchemy connection to MariaDB using environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST', 'localhost')

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

# Endpoint to create a user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], is_admin=data.get('is_admin', False))
    new_user.set_password(data['password'])  # Hash the password before saving
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

# Endpoint to create a message
@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.json
    new_message = UnhandledMessage(user_id=data['user_id'], message_text=data['message_text'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message created'}), 201

# Endpoint to get a specific user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    })

# Endpoint to get a specific user by username
@app.route('/api/users/username/<string:username>', methods=['GET'])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify({
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    })

# Endpoint to get all users
@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    } for user in users])

# Endpoint to get a specific message by ID
@app.route('/api/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = UnhandledMessage.query.get_or_404(message_id)
    return jsonify({
        'message_id': message.message_id,
        'user_id': message.user_id,
        'message_text': message.message_text,
        'created_at': message.created_at
    })

# Endpoint to get all messages
@app.route('/api/messages', methods=['GET'])
def get_all_messages():
    messages = UnhandledMessage.query.all()
    return jsonify([{
        'message_id': message.message_id,
        'user_id': message.user_id,
        'message_text': message.message_text,
        'created_at': message.created_at
    } for message in messages])

# Endpoint to get messages by user ID
@app.route('/api/messages/user/<int:user_id>', methods=['GET'])
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

