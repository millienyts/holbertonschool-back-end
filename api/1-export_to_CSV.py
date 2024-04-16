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
    # check if argv[1] is a number int, it means we are using argv
    if len(argv) > 1:
        try:
            id = int(argv[1])
        except ValueError:
            pass
            return

    if isinstance(id, int):
        user = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        to_dos = requests.get(
            f"https://jsonplaceholder.typicode.com/todos/?userId={id}"
            )

        if to_dos.status_code == 200 and user.status_code == 200:
            user = json.loads(user.text)
            to_dos = json.loads(to_dos.text)

            total_tasks = len(to_dos)
            tasks_completed = 0
            titles_completed = []
            csv_rows = []
            user_id = id

            for to_do in to_dos:
                # Prepare rows for csv file
                csv_rows.append(
                    [user_id, user['username'],
                     to_do['completed'],
                     to_do['title']
                     ]
                    )
                # Count and append titles of completed tasks
                if to_do['completed'] is True:
                    tasks_completed += 1
                    titles_completed.append(to_do['title'])

            tasks_completed = len(titles_completed)

            # Data of User Prints with tasks
            print(f"Employee {user['name']} is done \
                  with tasks({tasks_completed}/{total_tasks})")
            for title in titles_completed:
                print(f"\t {title}")

            with open(f"{user_id}.csv", 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                writer.writerows(csv_rows)


if __name__ == '__main__':
    get_employee()
