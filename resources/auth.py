import bcrypt
from flask import Blueprint, request, jsonify
from db.db_pool import get_connection, release_connection
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
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

        conn, cursor = get_connection()
        cursor.execute('SELECT id FROM users WHERE username=%s', (req['username'],))
        user = cursor.fetchone()
        if user:
            return jsonify({ 'message': 'This username already taken.' }), 422

        hashed_password = bcrypt.hashpw(req['password'].encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', (req['username'], hashed_password.decode('utf-8'), 'manager', None))
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
        return jsonify({ 'token': token, 'id': user['id'], 'username': user['username'], 'role': user['role'] }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to signin user.' }), 500
    finally:
        if conn:
            release_connection(conn)


@auth.route('/api/changepassword', methods=['PATCH'])
@jwt_required()
def change_password():
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager' and jwt_user['role'] != 'worker':
            return jsonify({ 'message': 'You are not manager or worker.' }), 403

        req = request.get_json()
        if len(req['oldPassword']) < 1 or len(req['oldPassword']) > 20:
            return jsonify({ 'message': 'Password must be between 1-20 characters.' }), 400
        if len(req['newPassword']) < 1 or len(req['newPassword']) > 20:
            return jsonify({ 'message': 'Password must be between 1-20 characters.' }), 400

        conn, cursor = get_connection()
        cursor.execute('SELECT id, password FROM users WHERE id=%s', (jwt_user['id'],))
        user_one = cursor.fetchone()
        if not user_one:
            return jsonify({ 'message': 'No user found.' }), 404

        is_valid_password = bcrypt.checkpw(req['oldPassword'].encode('utf-8'), user_one['password'].encode('utf-8'))
        if not is_valid_password:
            return jsonify({ 'message': 'Current password is incorrect.' }), 403

        hashed_password = bcrypt.hashpw(req['newPassword'].encode('utf-8'), bcrypt.gensalt())
        cursor.execute('UPDATE users SET password=%s WHERE id=%s', (hashed_password.decode('utf-8'), jwt_user['id']))
        conn.commit()
        return jsonify({ 'message': 'Password changed.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to change password.' }), 500
    finally:
        if conn:
            release_connection(conn)


@auth.route('/api/user/add', methods=['POST'])
@jwt_required()
def add_worker():
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager':
            return jsonify({ 'message': 'You are not manager.' }), 403

        req = request.get_json()
        if len(req['username']) < 1 or len(req['username']) > 20:
            return jsonify({ 'message': 'Username must be between 1-20 characters.' }), 400
        if len(req['password']) < 1 or len(req['password']) > 20:
            return jsonify({ 'message': 'Password must be between 1-20 characters.' }), 400

        conn, cursor = get_connection()
        cursor.execute('SELECT id FROM users WHERE username=%s', (req['username'],))
        user_one = cursor.fetchone()
        if user_one:
            return jsonify({ 'message': 'This username already taken.' }), 422

        hashed_password = bcrypt.hashpw(req['password'].encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', (req['username'], hashed_password.decode('utf-8'), 'worker', jwt_user['id']))
        conn.commit()
        return jsonify({ 'message': 'Worker added.' }), 201
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to add worker.' }), 500
    finally:
        if conn:
            release_connection(conn)
