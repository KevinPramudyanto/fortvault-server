import bcrypt
from flask import Blueprint, request, jsonify
from db.db_pool import get_connection, release_connection

auth = Blueprint('auth',__name__)

@auth.route('/api/signup', methods=['POST'])
def signup():
    conn = None
    try:
        req = request.get_json()
        if len(req['username']) > 20:
            return jsonify({ 'message': 'Username must be 20 characters or less.' }), 400
        if len(req['password']) > 20:
            return jsonify({ 'message': 'Password must be 20 characters or less.' }), 400
        if len(req['role']) > 20:
            return jsonify({ 'message': 'Role must be 20 characters or less.' }), 400


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
        print (error)
        return jsonify({ 'message': 'Failed to signup user.' }), 500
    finally:
        if conn:
            release_connection(conn)

