#!/usr/bin/python3
'''
    Api REST
'''

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

            for to_do in to_dos:
                
                if to_do['completed'] is True:
                    tasks_completed += 1
                    titles_completed.append(to_do['title'])

            tasks_completed = len(titles_completed)

            
            print(f"Employee {user['name']} is done \
                  with tasks({tasks_completed}/{total_tasks})")
            for title in titles_completed:
                print(f"\t {title}")

            # Data for json of a single user
            json_dict = {}
            user_list = []
            for task in to_dos:
                user_dict = {}
                user_dict.update(
                    {'task': task['title'],
                     'completed': task['completed'],
                     'username': user['username']}
                    )
                user_list.append(user_dict)
            json_dict[user['id']] = user_list

            with open(f"{user['id']}.json", 'w') as json_file:
                json.dump(json_dict, json_file)


if __name__ == '__main__':
    get_employee()
