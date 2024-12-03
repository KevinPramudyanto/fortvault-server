import os
import psycopg2.pool
import psycopg2.extras

pool = psycopg2.pool.SimpleConnectionPool(
    2,
    3,
    host=os.environ['DB_HOST'],
    database=os.environ['DB'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    port=os.environ['DB_PORT'],
)

def get_connection():
    conn = pool.getconn()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conn, cursor

def release_connection(connection):
    pool.putconn(connection)