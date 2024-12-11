import os
import requests
from flask import Blueprint, request, jsonify
from db.db_pool import get_connection, release_connection
from flask_jwt_extended import jwt_required, get_jwt

tool = Blueprint('tool',__name__)


@tool.route('/api/uploadtool', methods=['POST'])
@jwt_required()
def upload_tool():
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager':
            return jsonify({'message': 'You are not manager.'}), 403

        file = request.files['file']
        if not file:
            return jsonify({ 'message': 'Image is required.' }), 400

        r = requests.post(f"https://api.cloudinary.com/v1_1/{os.environ['CLOUD_NAME']}/image/upload", files={'file':file}, data={'upload_preset':os.environ['UPLOAD_PRESET']})

        if r.status_code != 200:
            return jsonify({ 'message': 'Failed to upload tool.' }), 500

        return jsonify({ 'public_id': r.json()['public_id'] }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to upload tool.' }), 500


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
        if len(req['image']) < 1 or len(req['image']) > 100:
            return jsonify({ 'message': 'Image must be between 1-100 characters.' }), 400

        conn, cursor = get_connection()
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', (req['name'], req['description'], req['brand'], req['image'], jwt_user['id'], None, True))
        conn.commit()
        return jsonify({ 'message': 'Tool created.' }), 201
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to create tool.' }), 500
    finally:
        if conn:
            release_connection(conn)


@tool.route('/api/tool', methods=['GET'])
@jwt_required()
def read_tools():
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
        cursor.execute('SELECT id, name, description, brand, image, manager, worker, approved FROM tools WHERE manager=%s ORDER BY name', (manager,))
        tools = cursor.fetchall()
        return jsonify(tools), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to read tools.' }), 500
    finally:
        if conn:
            release_connection(conn)


@tool.route('/api/tool/add/<tool_id>', methods=['GET'])
@jwt_required()
def add_tool(tool_id):
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'worker':
            return jsonify({ 'message': 'You are not worker.' }), 403

        conn, cursor = get_connection()
        cursor.execute('SELECT id, name, description, brand, image, manager, worker, approved FROM tools WHERE id=%s', (tool_id,))
        tool_one = cursor.fetchone()
        if not tool_one:
            return jsonify({ 'message': 'No tool found.' }), 404

        if tool_one['manager'] != jwt_user['manager']:
            return jsonify({ 'message': 'Unauthorized to add.' }), 403

        if tool_one['worker']:
            return jsonify({ 'message': 'Unauthorized to add.' }), 403

        cursor.execute('UPDATE tools SET worker=%s, approved=%s WHERE id=%s', (jwt_user['id'], False, tool_id))
        conn.commit()
        return jsonify({ 'message': 'Tool added.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to add tool.' }), 500
    finally:
        if conn:
            release_connection(conn)


@tool.route('/api/tool/remove/<tool_id>', methods=['GET'])
@jwt_required()
def remove_tool(tool_id):
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'worker':
            return jsonify({ 'message': 'You are not worker.' }), 403

        conn, cursor = get_connection()
        cursor.execute('SELECT id, name, description, brand, image, manager, worker, approved FROM tools WHERE id=%s', (tool_id,))
        tool_one = cursor.fetchone()
        if not tool_one:
            return jsonify({ 'message': 'No tool found.' }), 404

        if tool_one['manager'] != jwt_user['manager']:
            return jsonify({ 'message': 'Unauthorized to remove.' }), 403

        if tool_one['worker'] != jwt_user['id']:
            return jsonify({ 'message': 'Unauthorized to remove.' }), 403

        cursor.execute('UPDATE tools SET worker=%s, approved=%s WHERE id=%s', (None, True, tool_id))
        cursor.execute('UPDATE logs SET returned_at = CURRENT_TIMESTAMP WHERE worker_username=%s AND tool_name=%s AND returned_at IS NULL', (jwt_user['username'], tool_one['name']))
        conn.commit()
        return jsonify({ 'message': 'Tool removed.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to remove tool.' }), 500
    finally:
        if conn:
            release_connection(conn)


@tool.route('/api/tool/approve/<tool_id>', methods=['GET'])
@jwt_required()
def approve_tool(tool_id):
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager':
            return jsonify({ 'message': 'You are not manager.' }), 403

        conn, cursor = get_connection()
        cursor.execute('SELECT id, name, description, brand, image, manager, worker, approved FROM tools WHERE id=%s', (tool_id,))
        tool_one = cursor.fetchone()
        if not tool_one:
            return jsonify({ 'message': 'No tool found.' }), 404

        if tool_one['manager'] != jwt_user['id']:
            return jsonify({ 'message': 'Unauthorized to approve.' }), 403

        if tool_one['approved']:
            return jsonify({ 'message': 'Unauthorized to approve.' }), 403

        cursor.execute('SELECT id, username FROM users WHERE id=%s', (tool_one['worker'],))
        user_one = cursor.fetchone()

        cursor.execute('UPDATE tools SET approved=%s WHERE id=%s', (True, tool_id))
        cursor.execute('INSERT INTO logs (worker_username, tool_name, manager) VALUES (%s, %s, %s)', (user_one['username'], tool_one['name'], tool_one['manager']))
        conn.commit()
        return jsonify({ 'message': 'Tool approved.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to approve tool.' }), 500
    finally:
        if conn:
            release_connection(conn)


@tool.route('/api/tool/reject/<tool_id>', methods=['GET'])
@jwt_required()
def reject_tool(tool_id):
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager':
            return jsonify({ 'message': 'You are not manager.' }), 403

        conn, cursor = get_connection()
        cursor.execute('SELECT id, name, description, brand, image, manager, worker, approved FROM tools WHERE id=%s', (tool_id,))
        tool_one = cursor.fetchone()
        if not tool_one:
            return jsonify({ 'message': 'No tool found.' }), 404

        if tool_one['manager'] != jwt_user['id']:
            return jsonify({ 'message': 'Unauthorized to reject.' }), 403

        if tool_one['approved']:
            return jsonify({ 'message': 'Unauthorized to reject.' }), 403

        cursor.execute('UPDATE tools SET worker=%s, approved=%s WHERE id=%s', (None, True, tool_id))
        conn.commit()
        return jsonify({ 'message': 'Tool rejected.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to reject tool.' }), 500
    finally:
        if conn:
            release_connection(conn)


@tool.route('/api/tool/<tool_id>', methods=['GET'])
@jwt_required()
def read_tool(tool_id):
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager' and jwt_user['role'] != 'worker':
            return jsonify({ 'message': 'You are not manager or worker.' }), 403

        conn, cursor = get_connection()
        cursor.execute('SELECT id, name, description, brand, image, manager, worker, approved FROM tools WHERE id=%s', (tool_id,))
        tool_one = cursor.fetchone()
        if not tool_one:
            return jsonify({ 'message': 'No tool found.' }), 404

        if jwt_user['role'] == 'manager' and tool_one['manager'] != jwt_user['id']:
            return jsonify({ 'message': 'Unauthorized to read.' }), 403

        if jwt_user['role'] == 'worker' and tool_one['manager'] != jwt_user['manager']:
            return jsonify({ 'message': 'Unauthorized to read.' }), 403

        return jsonify(tool_one), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to read tool.' }), 500
    finally:
        if conn:
            release_connection(conn)


@tool.route('/api/tool/<tool_id>', methods=['PATCH'])
@jwt_required()
def update_tool(tool_id):
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

        conn, cursor = get_connection()
        cursor.execute('SELECT id, name, description, brand, image, manager, worker, approved FROM tools WHERE id=%s', (tool_id,))
        tool_one = cursor.fetchone()
        if not tool_one:
            return jsonify({ 'message': 'No tool found.' }), 404

        if tool_one['manager'] != jwt_user['id']:
            return jsonify({ 'message': 'Unauthorized to update.' }), 403

        if not tool_one['approved']:
            return jsonify({ 'message': 'Unable to update before approving/rejecting tool.' }), 422

        if tool_one['worker']:
            return jsonify({ 'message': 'Unable to update before worker returning tool.' }), 422

        cursor.execute('UPDATE tools SET name=%s, description=%s, brand=%s WHERE id=%s', (req['name'], req['description'], req['brand'], tool_id))
        conn.commit()
        return jsonify({ 'message': 'Tool updated.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to update tool.' }), 500
    finally:
        if conn:
            release_connection(conn)


@tool.route('/api/tool/<tool_id>', methods=['DELETE'])
@jwt_required()
def delete_tool(tool_id):
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager':
            return jsonify({ 'message': 'You are not manager.' }), 403

        conn, cursor = get_connection()
        cursor.execute('SELECT id, name, description, brand, image, manager, worker, approved FROM tools WHERE id=%s', (tool_id,))
        tool_one = cursor.fetchone()
        if not tool_one:
            return jsonify({ 'message': 'No tool found.' }), 404

        if tool_one['manager'] != jwt_user['id']:
            return jsonify({ 'message': 'Unauthorized to delete.' }), 403

        if not tool_one['approved']:
            return jsonify({ 'message': 'Unable to delete before approving/rejecting tool.' }), 422

        if tool_one['worker']:
            return jsonify({ 'message': 'Unable to delete before worker returning tool.' }), 422

        cursor.execute('DELETE FROM tools WHERE id=%s', (tool_id,))
        conn.commit()
        return jsonify({ 'message': 'Tool deleted.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to delete tool.' }), 500
    finally:
        if conn:
            release_connection(conn)
