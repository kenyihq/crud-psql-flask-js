from flask import Flask, request, jsonify
from psycopg2 import extras

# Import from file database.py
from database import get_connection

app = Flask(__name__)


@app.route('/', )
def home():
    conn = get_connection()
    cur = conn.cursor()

    result = cur.execute("SELECT 1 + 1")
    print(result)
    return 'Hello World!'


@app.get('/api/users')
def get_users():
    return 'getting users'


@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = new_user['password']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING *",
                (username, email, password))

    new_created_user = cur.fetchone()
    print(new_created_user)


    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_created_user)


@app.put('/api/users/1')
def update_user():
    return 'updating users'


@app.delete('/api/users/1')
def delete_user():
    return 'deleting users'


@app.get('/api/users/1')
def get_user():
    return 'getting users'


if __name__ == '__main__':
    app.run(debug=True)
