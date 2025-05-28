from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'super_secret_key'

db_config_init = {
    'host': 'db',
    'user': 'root',
    'password': 'root',
}

db_config = {
    'host': 'db',
    'user': 'root',
    'password': 'root',
    'database': 'sqlinjection_demo'
}

def get_db_connection(config=None):
    try:
        connection = mysql.connector.connect(**(config or db_config))
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    connection = get_db_connection(db_config_init)
    if not connection:
        print('--------')

        return False
    
    try:
        cursor = connection.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS sqlinjection_demo")
        
        cursor.execute("USE sqlinjection_demo")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        )
        """)
        
        users_data = [
            (1,'admin', 'admin123', 'admin@example.com', True),
            (2,'user1', 'password1', 'user1@example.com', False),
            (3,'user2', 'password2', 'user2@example.com', False),
            (4,'test', 'test123', 'test@example.com', False)
        ]
        
        cursor.execute("DELETE FROM users")
        
        insert_query = "INSERT INTO users (id, username, password, email, is_admin) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, users_data)
        
        connection.commit()
        return True
        
    except Error as e:
        print(e)
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/init-db', methods=['POST'])
def initialize_db():
    if init_database():
        flash('База данных успешно инициализирована!', 'success')
    else:
        flash('Ошибка при инициализации базы данных', 'danger')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    users = []
    search_query = ""
    
    if request.method == 'POST' and 'search' in request.form:
        search_query = request.form.get('search', '')
        
        query = f"SELECT * FROM users WHERE username = '{search_query}'"
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query)
                users = cursor.fetchall()
                
                if not users:
                    flash('Пользователь не найден', 'info')
            except Error as e:
                flash(f'Ошибка базы данных: {e}', 'danger')
            finally:
                cursor.close()
                connection.close()
    
    return render_template('index.html', users=users, search_query=search_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)