from flask import Blueprint, request, jsonify
from db.db_pool import get_connection, release_connection
from flask_jwt_extended import jwt_required, get_jwt

user = Blueprint('user',__name__)


@user.route('/api/user/add', methods=['PATCH'])
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

        conn, cursor = get_connection()
        cursor.execute('SELECT id, manager FROM users WHERE username=%s AND role=%s', (req['username'],'worker'))
        user_one = cursor.fetchone()
        if not user_one:
            return jsonify({ 'message': 'No worker found.' }), 404

        if user_one['manager']:
            return jsonify({ 'message': 'Unauthorized to add.' }), 403

        cursor.execute('UPDATE users SET manager=%s WHERE id=%s', (jwt_user['id'], user_one['id']))
        conn.commit()
        return jsonify({ 'message': 'Worker added.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to add worker.' }), 500
    finally:
        if conn:
            release_connection(conn)


@user.route('/api/user/get', methods=['GET'])
@jwt_required()
def get_workers():
    conn = None
    try:
        jwt_user = get_jwt()
        manager = None
        if jwt_user['role'] == 'manager':
            manager = jwt_user['id']
        elif jwt_user['role'] == 'worker':
            manager = jwt_user['manager']
        else:
            return jsonify({ 'message': 'You are not manager or worker.' }), 403

        conn, cursor = get_connection()
        cursor.execute('SELECT id, username FROM users WHERE role=%s AND manager=%s', ('worker', manager))
        users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to get your workers.' }), 500
    finally:
        if conn:
            release_connection(conn)


@user.route('/api/user/remove/<user_id>', methods=['GET'])
@jwt_required()
def remove_worker(user_id):
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager':
            return jsonify({ 'message': 'You are not manager.' }), 403

        conn, cursor = get_connection()
        cursor.execute('SELECT id, manager FROM users WHERE id=%s', (user_id,))
        user_one = cursor.fetchone()
        if not user_one:
            return jsonify({ 'message': 'No worker found.' }), 404

        if user_one['manager'] != jwt_user['id']:
            return jsonify({ 'message': 'Unauthorized to remove.' }), 403

        cursor.execute('SELECT id FROM tools WHERE worker=%s', (user_one['id'],))
        tool_one = cursor.fetchone()
        if tool_one:
            return jsonify({ 'message': 'Unable to remove before user returns their tools.' }), 422

        cursor.execute('UPDATE users SET manager=%s WHERE id=%s', (None, user_one['id']))
        conn.commit()
        return jsonify({ 'message': 'Worker removed.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to remove worker.' }), 500
    finally:
        if conn:
            release_connection(conn)
