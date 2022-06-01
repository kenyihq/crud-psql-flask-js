from flask import Flask, request, jsonify, send_file
from psycopg2 import extras
from cryptography.fernet import Fernet 

# Import from file database.py
from database import get_connection

app = Flask(__name__)
key = Fernet.generate_key()




@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(users)


@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))

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


@app.put('/api/users/<id>')
def update_user(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))

    cur.execute("UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s RETURNING *",
                (username, email, password, id))
    updated_user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if updated_user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(updated_user)


@app.delete('/api/users/<id>')
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (id,))
    user = cur.fetchone()
    print(user)
    conn.commit()
    conn.close()
    cur.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)


@app.get('/api/users/<id>')
def get_user(id):
    conn = get_connection()    
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)

@app.route('/', )
def home():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True)
