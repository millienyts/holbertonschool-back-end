from flask import Flask, request, jsonify
import requests
import csv
import json

app = Flask(__name__)

@app.route('/gather_data/<int:employee_id>', methods=['GET'])
def gather_data(employee_id):
    api_url = f'https://jsonplaceholder.typicode.com/todos?userId={employee_id}'
    response = requests.get(api_url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from the API'}), 500

    todo_list = response.json()
    employee_name = todo_list[0]['username']  # Assuming username is available in the response
    completed_tasks = [task for task in todo_list if task['completed']]
    num_completed_tasks = len(completed_tasks)
    total_tasks = len(todo_list)

    # Format response
    response_data = {
        'employee_name': employee_name,
        'completed_tasks': num_completed_tasks,
        'total_tasks': total_tasks,
        'completed_task_titles': [task['title'] for task in completed_tasks]
    }

    return jsonify(response_data), 200

# Task 1 Endpoint
@app.route('/export_to_csv/<int:employee_id>', methods=['GET'])
def export_to_csv(employee_id):
    # Fetch data from Task 0 endpoint
    response = gather_data(employee_id)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'}), 500

    data = response.json()
    employee_name = data['employee_name']
    completed_task_titles = data['completed_task_titles']

    # Write data to CSV file
    filename = f'{employee_id}.csv'
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['USER_ID', 'USERNAME', 'TASK_COMPLETED_STATUS', 'TASK_TITLE'])
        for task_title in completed_task_titles:
            csv_writer.writerow([employee_id, employee_name, 'True', task_title])

    return jsonify({'message': f'Data exported to {filename}'}), 200

@app.route('/export_to_json/<int:employee_id>', methods=['GET'])
def export_to_json(employee_id):
    # Fetch data from Task 0 endpoint
    response = gather_data(employee_id)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'}), 500

    data = response.json()
    employee_name = data['employee_name']
    completed_task_titles = data['completed_task_titles']

    # Write data to JSON file
    filename = f'{employee_id}.json'
    json_data = {str(employee_id): [{'task': task_title, 'completed': True, 'username': employee_name} for task_title in completed_task_titles]}
    with open(filename, 'w') as jsonfile:
        json.dump(json_data, jsonfile)

    return jsonify({'message': f'Data exported to {filename}'}), 200

if __name__ == '__main__':
    app.run(debug=True)
