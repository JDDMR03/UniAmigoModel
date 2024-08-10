from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLAlchemy connection to MariaDB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:200723@localhost/uniamigo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Define the UnhandledMessage model
class UnhandledMessage(db.Model):
    __tablename__ = 'unhandled_messages'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('messages', lazy=True))

# Example endpoint to create a user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], password=data['password'], is_admin=data.get('is_admin', False))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

# Example endpoint to create a message
@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.json
    new_message = UnhandledMessage(user_id=data['user_id'], message_text=data['message_text'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message created'}), 201

if __name__ == '__main__':
    app.run(debug=True)

