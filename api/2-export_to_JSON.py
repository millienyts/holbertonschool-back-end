#!/usr/bin/python3
'''
    This script interacts with a REST API to retrieve information about an employee's TODO list progress.
'''

import json
import requests
from sys import argv

def get_employee(id=None):
    '''
    Retrieves and displays information about an employee's tasks based on the employee ID.
    If no ID is provided, it retrieves tasks based on the command line argument.
    '''

    # Check if an ID is provided as a command line argument
    if len(argv) > 1:
        try:
            id = int(argv[1])
        except ValueError:
            pass
            return

    # Retrieve employee data and their corresponding tasks
    if isinstance(id, int):
        user_response = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        tasks_response = requests.get(f"https://jsonplaceholder.typicode.com/todos/?userId={id}")

        if tasks_response.status_code == 200 and user_response.status_code == 200:
            user = json.loads(user_response.text)
            tasks = json.loads(tasks_response.text)

            total_tasks = len(tasks)
            tasks_completed = 0
            completed_task_titles = []

            # Count completed tasks and store their titles
            for task in tasks:
                if task['completed']:
                    tasks_completed += 1
                    completed_task_titles.append(task['title'])

            tasks_completed = len(completed_task_titles)

            # Print employee's task completion status
            print(f"Employee {user['name']} has completed {tasks_completed}/{total_tasks} tasks:")
            for title in completed_task_titles:
                print(f"\t {title}")

            # Prepare data for JSON output
            json_data = {}
            tasks_data = []
            for task in tasks:
                task_data = {
                    'task': task['title'],
                    'completed': task['completed'],
                    'username': user['username']
                }
                tasks_data.append(task_data)
            json_data[user['id']] = tasks_data

            # Write JSON data to a file
            with open(f"{user['id']}.json", 'w') as json_file:
                json.dump(json_data, json_file)

if __name__ == '__main__':
    get_employee()

