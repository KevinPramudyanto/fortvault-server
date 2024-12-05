import bcrypt
from flask import Blueprint, request, jsonify
from db.db_pool import get_connection, release_connection
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth = Blueprint('auth',__name__)


@auth.route('/api/signup', methods=['POST'])
def signup():
    conn = None
    try:
        req = request.get_json()
        if len(req['username']) < 1 or len(req['username']) > 20:
            return jsonify({ 'message': 'Username must be between 1-20 characters.' }), 400
        if len(req['password']) < 1 or len(req['password']) > 20:
            return jsonify({ 'message': 'Password must be between 1-20 characters.' }), 400
        if len(req['role']) < 1 or len(req['role']) > 10:
            return jsonify({ 'message': 'Role must be between 1-10 characters.' }), 400

        conn, cursor = get_connection()
        cursor.execute('SELECT id FROM users WHERE username=%s', (req['username'],))
        user = cursor.fetchone()
        if user:
            return jsonify({ 'message': 'This username already taken.' }), 422

        hashed_password = bcrypt.hashpw(req['password'].encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', (req['username'], hashed_password.decode('utf-8'), req['role'], None))
        conn.commit()
        return jsonify({ 'message': 'User created.' }), 201
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to signup user.' }), 500
    finally:
        if conn:
            release_connection(conn)


@auth.route('/api/signin', methods=['POST'])
def signin():
    conn = None
    try:
        req = request.get_json()
        if len(req['username']) < 1 or len(req['username']) > 20:
            return jsonify({ 'message': 'Username must be between 1-20 characters.' }), 400
        if len(req['password']) < 1 or len(req['password']) > 20:
            return jsonify({ 'message': 'Password must be between 1-20 characters.' }), 400

        conn, cursor = get_connection()
        cursor.execute('SELECT id, username, password, role, manager FROM users WHERE username=%s', (req['username'],))
        user = cursor.fetchone()
        if not user:
            return jsonify({ 'message': 'Incorrect username or password.' }), 401

        is_valid_password = bcrypt.checkpw(req['password'].encode('utf-8'), user['password'].encode('utf-8'))
        if not is_valid_password:
            return jsonify({ 'message': 'Incorrect username or password.' }), 401

        claims = { 'id': user['id'], 'username': user['username'], 'role': user['role'], 'manager': user['manager'] }
        token = create_access_token(identity=user['id'], additional_claims=claims, expires_delta=timedelta(hours=1))
        return jsonify({ 'token': token, 'id': user['id'], 'role': user['role'] }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to signin user.' }), 500
    finally:
        if conn:
            release_connection(conn)


