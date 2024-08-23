from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row  # Para acessar os resultados como dicionários
    return conn

# Rota para criar a tabela (opcional, apenas para fins de exemplo)
@app.route('/create-table')
def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()
    return "Tabela criada com sucesso!"

# Rota para inserir dados
@app.route('/add-user', methods=['POST'])
def add_user():
    name = request.json['name']
    conn = get_db_connection()
    conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return "Usuário adicionado com sucesso!"

# Rota para consultar todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    
    users_list = []
    for user in users:
        users_list.append({"id": user["id"], "name": user["name"]})
    
    return jsonify(users_list)

# Rota para consultar um usuário específico pelo ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if user is None:
        return "Usuário não encontrado", 404
    
    return jsonify({"id": user["id"], "name": user["name"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
