#!/usr/bin/python3
""" Script to extract and export data in csv format"""
import requests
import sys
import csv
import json
if __name__ == "__main__":
	url = "https://jsonplaceholder.typicode.com/"
	user = requests.get(url + "users/{}".format(sys.argv[1])).json()
	todos = requests.get(url + "todos", params={"userId": sys.argv[1]}).json()
	USERNAME = user["username"]
	filename = sys.argv[1]
	USER_ID = sys.argv[1]

	with open("{}.json".format(filename), "w" ) as jsonf:
        # write rows
		for task in todos:
			json.dump({
				USER_ID: [{"task":task.get("title"), "completed": task.get("completed"),
							"username":USERNAME}]}, jsonf)
	
