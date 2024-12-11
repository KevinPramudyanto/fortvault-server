from flask import Blueprint, jsonify
from db.db_pool import get_connection, release_connection
from flask_jwt_extended import jwt_required, get_jwt

logs = Blueprint('logs',__name__)


@logs.route('/api/logs/worker', methods=['GET'])
@jwt_required()
def tools_by_worker():
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager':
            return jsonify({ 'message': 'You are not manager.' }), 403

        conn, cursor = get_connection()
        cursor.execute("SELECT worker_username, COUNT(CASE WHEN DATE_TRUNC('month', borrowed_at) = DATE_TRUNC('month', CURRENT_TIMESTAMP - INTERVAL '1 month') THEN 1 END) AS last_month, COUNT(CASE WHEN DATE_TRUNC('month', borrowed_at) = DATE_TRUNC('month', CURRENT_TIMESTAMP - INTERVAL '2 months') THEN 1 END) AS two_months_ago, COUNT(CASE WHEN DATE_TRUNC('month', borrowed_at) = DATE_TRUNC('month', CURRENT_TIMESTAMP - INTERVAL '3 months') THEN 1 END) AS three_months_ago FROM logs WHERE manager=%s GROUP BY worker_username ORDER BY last_month DESC", (jwt_user['id'],))
        logs_all = cursor.fetchall()
        return jsonify(logs_all), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to get worker logs.' }), 500
    finally:
        if conn:
            release_connection(conn)


@logs.route('/api/logs/tool', methods=['GET'])
@jwt_required()
def tools_by_time():
    conn = None
    try:
        jwt_user = get_jwt()
        if jwt_user['role'] != 'manager':
            return jsonify({ 'message': 'You are not manager.' }), 403

        conn, cursor = get_connection()
        cursor.execute("SELECT TO_CHAR(DATE_TRUNC('month', borrowed_at), 'Mon YYYY') AS borrow_month, COUNT(*) AS borrow_count FROM logs WHERE manager=%s AND DATE_TRUNC('month', borrowed_at) < DATE_TRUNC('month', CURRENT_TIMESTAMP) GROUP BY DATE_TRUNC('month', borrowed_at) ORDER BY DATE_TRUNC('month', borrowed_at)", (jwt_user['id'],))
        logs_all = cursor.fetchall()
        return jsonify(logs_all), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Failed to get tool logs.' }), 500
    finally:
        if conn:
            release_connection(conn)
