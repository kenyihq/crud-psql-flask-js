from flask import Flask
from psycopg2 import connect

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

if __name__ == '__main__':
    app.run(debug=True)