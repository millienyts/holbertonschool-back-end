#!/usr/bin/python3
'''
    Api REST
'''

import csv
import json
import requests
from sys import argv


def get_employee(id=None):
    '''
        using this REST API, for a given employee ID,
        returns information about his/her TODO list progress.
    '''
    # If an ID is provided as a command-line argument, use it
    if len(argv) > 1:
        try:
            id = int(argv[1])
        except ValueError:
            pass

    # If ID is provided or obtained from command-line, proceed
    if isinstance(id, int):
        # Fetch user data and todo list for the given ID
        user_response = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        todos_response = requests.get(f"https://jsonplaceholder.typicode.com/todos/?userId={id}")

        # Check if responses are successful
        if user_response.status_code == 200 and todos_response.status_code == 200:
            user_data = user_response.json()
            todos_data = todos_response.json()

            # Extract relevant information
            total_tasks = len(todos_data)
            completed_tasks = [todo for todo in todos_data if todo['completed']]
            num_completed_tasks = len(completed_tasks)
            completed_task_titles = [todo['title'] for todo in completed_tasks]

            # Print user information and completed tasks
            print(f"Employee {user_data['name']} is done with tasks({num_completed_tasks}/{total_tasks}):")
            for title in completed_task_titles:
                print(f"\t{title}")

            # Write data to CSV file
            with open(f"{id}.csv", 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['USER_ID', 'USERNAME', 'TASK_COMPLETED_STATUS', 'TASK_TITLE'])
                for todo in todos_data:
                    csv_writer.writerow([id, user_data['username'], todo['completed'], todo['title']])

if __name__ == '__main__':
    get_employee()
