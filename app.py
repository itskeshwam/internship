from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
import os

app = Flask(__name__, static_folder='static')

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'company'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    name = data['name']
    department = data['department']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Employee (name, department) VALUES (%s, %s)', (name, department))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Employee added successfully!'}), 201

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    name = data['name']
    department = data['department']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Employee SET name = %s, department = %s WHERE id = %s', (name, department, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Employee updated successfully!'})

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Employee WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Employee deleted successfully!'})

@app.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Employee')
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    employee_list = []
    for emp in employees:
        employee_list.append({
            'id': emp[0],
            'name': emp[1],
            'department': emp[2]
        })
    return jsonify(employee_list)

if __name__ == '__main__':
    app.run(debug=True)
