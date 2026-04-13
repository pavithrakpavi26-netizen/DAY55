import json
from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [
    {'id': 1, 'name': 'Ashley'},
    {'id': 2, 'name': 'Kate'},
    {'id': 3, 'name': 'Joe'}
]

nextEmployeeId = 4

# Home route (added fix)
@app.route('/')
def home():
    return "Employee API is running"

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    return jsonify(employee)

def get_employee(id):
    return next((e for e in employees if e['id'] == id), None)

def employee_is_valid(employee):
    if "name" not in employee:
        return False
    return True

@app.route('/employees', methods=['POST'])
def create_employee():
    global nextEmployeeId

    employee = request.get_json()

    if not employee_is_valid(employee):
        return jsonify({'error': 'Invalid employee properties'}), 400

    employee['id'] = nextEmployeeId
    nextEmployeeId += 1

    employees.append(employee)

    return jsonify(employee), 201

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = get_employee(id)

    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404

    data = request.get_json()

    employee['name'] = data.get('name', employee['name'])

    return jsonify(employee)

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    global employees

    employee = get_employee(id)

    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404

    employees = [e for e in employees if e['id'] != id]

    return jsonify({'message':'Deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)