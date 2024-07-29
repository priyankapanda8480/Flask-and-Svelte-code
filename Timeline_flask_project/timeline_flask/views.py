from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import hashlib
import secrets
import jwt as pyjwt
from .models import db, User, Post  
SECRET_KEY = 'your_jwt_secret_key'

views_blueprint = Blueprint('views', __name__)

def generate_jwt(user):
    try:
        expiration = datetime.utcnow() + timedelta(hours=1)
        token = pyjwt.encode({
            'username': user.username,
            'uid': user.uid,
            'exp': expiration
        }, SECRET_KEY, algorithm='HS256')
        print("Generated token:", token)
        return token
    except Exception as e:
        print(f"Error generating JWT: {e}")
        raise

def hash_password(password, salt):
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password

@views_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        print(f"Email: {email}, Password: {password}")  

        user = authenticate(email, password)
        if user:
            token = create_access_token(identity=user.uid)
            response_data = {
                'message': 'Login successful',
                'token': token,
                'uid': user.uid 
            }
            response_data = make_response(jsonify(response_data))
            response_data.set_cookie('jwt', token, httponly=True, secure=True)
            return response_data
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@views_blueprint.route('/register', methods=['POST'])   

def register():
    data = request.get_json()
    username = data.get('username')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    country = data.get('country')
    fullname = data.get('fullname')
    password = data.get('password')
    date_of_birth = data.get('dateOfBirth')  

    if not username or not password or not fullname or not firstname or not lastname or not email or not country or not date_of_birth:
        return jsonify({'message': 'All fields are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    salt = secrets.token_hex(16)
    hashed_password = hash_password(password, salt)

    try:
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

    new_user = User(
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        country=country,
        fullname=fullname,
        password=hashed_password,
        salt=salt,
        date_of_birth=date_of_birth
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


    
@views_blueprint.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        data = request.get_json()
        print("Received data:", data)
        current_user_id = get_jwt_identity()  # Use get_jwt_identity to get the current user ID
        print("Current user ID:", current_user_id)

        if not data or not data.get('title') or not data.get('content'):
            return jsonify({'message': 'Missing title or content'}), 400

        post = Post(
            title=data['title'],
            content=data['content'],
            user_id=current_user_id
        )

        db.session.add(post)
        db.session.commit()

        return jsonify({'message': 'Post created successfully'}), 201
    except Exception as e:
        print(f"Error creating post: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@views_blueprint.route('/api/timeline', methods=['GET'])
@jwt_required()
def get_timeline():
    try:
        current_user_id = get_jwt_identity()
        print("Fetching posts for user ID:", current_user_id)
        
        user_posts = Post.query.filter_by(user_id=current_user_id).all()
        posts_data = [
            {
                'id': post.uid,
                'title': post.title,
                'content': post.content
            }
            for post in user_posts
        ]

        return jsonify(posts_data), 200
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return jsonify({'message': 'Internal server error'}), 500





def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        stored_salt = user.salt
        stored_hashed_password = user.password
        hashed_password = hash_password(password, stored_salt)
        if hashed_password == stored_hashed_password:
            return user
    return False