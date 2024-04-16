#!/usr/bin/python3
'''
    Api REST
'''

import json
import requests
from sys import argv

def get_employee(id=None):
    '''
        Function to retrieve employee information
        using a REST API, based on the given employee ID.
    '''
    # Check if an ID is provided as a command line argument
    if len(argv) > 1:
        try:
            id = int(argv[1])  # Set id to the provided command line argument
        except ValueError:
            pass
            return

    if isinstance(id, int):
        # Retrieve user information
        user = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        # Retrieve todo list for the user
        to_dos = requests.get(f"https://jsonplaceholder.typicode.com/todos/?userId={id}")

        # Check if requests were successful
        if to_dos.status_code == 200 and user.status_code == 200:
            # Convert response text to JSON format
            user = json.loads(user.text)
            to_dos = json.loads(to_dos.text)

            total_tasks = len(to_dos)
            tasks_completed = 0
            titles_completed = []

            # Count completed tasks and collect their titles
            for to_do in to_dos:
                if to_do['completed'] is True:
                    tasks_completed += 1
                    titles_completed.append(to_do['title'])

            tasks_completed = len(titles_completed)

            # Print employee's task completion status
            print(f"Employee {user['name']} has completed tasks ({tasks_completed}/{total_tasks}):")
            for title in titles_completed:
                print(f"\t {title}")

            # Prepare data for JSON file
            json_dict = {}
            user_list = []
            for task in to_dos:
                user_dict = {'task': task['title'],
                             'completed': task['completed'],
                             'username': user['username']}
                user_list.append(user_dict)
            json_dict[user['id']] = user_list

            # Write JSON data to a file
            with open(f"{user['id']}.json", 'w') as json_file:
                json.dump(json_dict, json_file)


if __name__ == '__main__':
    get_employee()
