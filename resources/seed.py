from flask import Blueprint, jsonify
from db.db_pool import get_connection, release_connection

seed = Blueprint('seed',__name__)


@seed.route('/api/seed', methods=['GET'])
def seed_all():
    conn = None
    try:
        conn, cursor = get_connection()

        cursor.execute('DELETE FROM tools')
        cursor.execute('DELETE FROM logs')
        cursor.execute('DELETE FROM users')

        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('store1', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'manager', None))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('store2', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'manager', None))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('store3', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'manager', None))

        cursor.execute('SELECT id FROM users WHERE username=%s', ('store1',))
        manager_one = cursor.fetchone()
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('worker1', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'worker', manager_one['id']))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('worker2', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'worker', manager_one['id']))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('worker3', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'worker', manager_one['id']))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('worker4', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'worker', manager_one['id']))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('worker5', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'worker', manager_one['id']))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('worker6', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'worker', manager_one['id']))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('worker7', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'worker', manager_one['id']))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('worker8', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'worker', manager_one['id']))
        cursor.execute('INSERT INTO users (username, password, role, manager) VALUES (%s, %s, %s, %s)', ('worker9', '$2b$12$i9K0zzNpUvgyk3tZ3dssdupj5uchbDePYPAg/Zu70Yt0bRPa9mOwe', 'worker', manager_one['id']))

        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', ('tool1', 'description1', 'brand1', 'https://picsum.photos/id/50/1600/900', manager_one['id'], None, True))
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', ('tool2', 'description2', 'brand2', 'https://picsum.photos/id/100/1600/900', manager_one['id'], None, True))
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', ('tool3', 'description3', 'brand3', 'https://picsum.photos/id/152/1600/900', manager_one['id'], None, True))
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', ('tool4', 'description4', 'brand4', 'https://picsum.photos/id/200/1600/900', manager_one['id'], None, True))
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', ('tool5', 'description5', 'brand5', 'https://picsum.photos/id/250/1600/900', manager_one['id'], None, True))
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', ('tool6', 'description6', 'brand6', 'https://picsum.photos/id/301/1600/900', manager_one['id'], None, True))
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', ('tool7', 'description7', 'brand7', 'https://picsum.photos/id/350/1600/900', manager_one['id'], None, True))
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', ('tool8', 'description8', 'brand8', 'https://picsum.photos/id/400/1600/900', manager_one['id'], None, True))
        cursor.execute('INSERT INTO tools (name, description, brand, image, manager, worker, approved) VALUES (%s, %s, %s, %s, %s, %s, %s)', ('tool9', 'description9', 'brand9', 'https://picsum.photos/id/450/1600/900', manager_one['id'], None, True))

        for num in range(200):
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool1', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool2', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool3', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool4', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool5', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool6', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool7', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool8', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool9', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool1', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker1', 'tool2', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker2', 'tool3', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker2', 'tool4', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker2', 'tool5', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker2', 'tool6', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker2', 'tool7', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker2', 'tool8', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker2', 'tool9', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker3', 'tool1', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker3', 'tool2', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker3', 'tool3', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker3', 'tool4', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker3', 'tool5', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker4', 'tool6', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker4', 'tool7', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker4', 'tool8', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker5', 'tool9', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker5', 'tool1', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker6', 'tool2', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker7', 'tool3', manager_one['id']))
            cursor.execute("INSERT INTO logs (worker_username, tool_name, manager, borrowed_at, returned_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP - (random() * INTERVAL '330 days'), CURRENT_TIMESTAMP)",('worker8', 'tool4', manager_one['id']))

        conn.commit()
        return jsonify({ 'message': 'Seed successful.' }), 200
    except Exception as error:
        print(error)
        return jsonify({ 'message': 'Seed failed.' }), 500
    finally:
        if conn:
            release_connection(conn)
