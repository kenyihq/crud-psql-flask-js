from flask import Flask

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
    return 'creating users'

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