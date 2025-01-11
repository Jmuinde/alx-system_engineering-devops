#!/usr/bin/python3
""" Script to extract and export data in csv format"""
import requests
import sys
import csv
import json
if __name__ == "__main__":
	url = "https://jsonplaceholder.typicode.com/"
	user = requests.get(url + "users/").json()
	todos = requests.get(url + "todos", params={"userId": user.get("id")}).json()
	filename = "todo_all_employees"

	with open("{}.json".format(filename), "w" ) as jsonf:
        # write rows
		for task in todos:
			for u in user:
				json.dump({
					u.get("id"): [{"username": u.get("username"), "task":task.get("title"), "completed": task.get("completed")}]}, jsonf)
	
