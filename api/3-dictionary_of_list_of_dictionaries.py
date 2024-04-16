#!/usr/bin/python3
"""Documentation"""
import json
import requests

api_users_url = 'https://jsonplaceholder.typicode.com/users'
api_todos_url = 'https://jsonplaceholder.typicode.com/todos'

# Fetch user data
response = requests.get(api_users_url)
users = response.json()

# Extract user IDs
user_ids = [user['id'] for user in users]

# Create a session for efficient HTTP requests
with requests.Session() as session:
    json_dict = {}

    for idx, user in enumerate(users, 1):
        # Fetch user data and todos in a single request
        response = session.get(f"{api_users_url}/{user['id']}", params={'_embed': 'todos'})
        if response.status_code != 200:
            print(f"Failed to fetch data for user {user['id']}")
            continue
        
        user_data = response.json()
        todos = user_data.get('todos', [])
        
        # Extract relevant information and construct JSON data
        json_dict[user['id']] = [{'username': user_data['username'], 'task': todo['title'], 'completed': todo['completed']} for todo in todos]

# Write data to JSON file
with open("todo_all_employees.json", 'w') as json_file:
    json.dump(json_dict, json_file)
