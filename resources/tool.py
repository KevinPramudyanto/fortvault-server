from flask import Blueprint, request, jsonify
from db.db_pool import get_connection, release_connection
from flask_jwt_extended import jwt_required, get_jwt

tool = Blueprint('tool',__name__)


@tool.route('/api/tool', methods=['POST'])
@jwt_required()
def create_tool():
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager':
            return jsonify({ 'message': 'You are not manager.' }), 403

        req = request.get_json()
        if len(req['name']) < 1 or len(req['name']) > 50:
            return jsonify({ 'message': 'Name must be between 1-50 characters.' }), 400
        if len(req['description']) < 1 or len(req['description']) > 200:
            return jsonify({ 'message': 'Description must be between 1-200 characters.' }), 400
        if len(req['brand']) < 1 or len(req['brand']) > 50:
            return jsonify({ 'message': 'Brand must be between 1-50 characters.' }), 400
        if len(req['image']) < 1 or len(req['image']) > 50:
            return jsonify({ 'message': 'Image must be between 1-50 characters.' }), 400

        conn, cursor = get_connection()
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', (req['name'], req['description'], req['brand'], req['image'], jwt_user['id'], None, True))
        conn.commit()
        return jsonify({ 'message': 'Tool created.' }), 201
    except Exception as error:
        print (error)
        return jsonify({ 'message': 'Failed to create tool.' }), 500
    finally:
        if conn:
            release_connection(conn)

