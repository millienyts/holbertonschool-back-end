#!/usr/bin/python3
"""Dictionary"""
import json
import requests

api_users_url = 'https://jsonplaceholder.typicode.com/users'
api_todos_url = 'https://jsonplaceholder.typicode.com/todos'

response = requests.get(api_users_url)
users = response.json()

user_ids = []
for user in users:
    user_ids.append(user["id"])

json_dict = {}

for employee_id in user_ids:
    api_url = f'https://jsonplaceholder.typicode.com/users/{employee_id}'
    response = requests.get(api_url)

    employee_name = response.json()["username"]

    api_url2 = (
        f'https://jsonplaceholder.typicode.com/todos?userId={employee_id}'
        )
    response = requests.get(api_url2)

    tasks = response.json()

    json_dict[employee_id] = []
    for task in tasks:
        json_format = {
            "username": employee_name,
            "task": task["title"],
            "completed": task["completed"]
        }
        json_dict[employee_id].append(json_format)

with open("todo_all_employees.json", 'w') as json_file:
    json.dump(json_dict, json_file)
