#!/usr/bin/python3
""" Script to extract and export data in csv format"""
import requests
import sys
import csv

if __name__ == "__main__":
	url = "https://jsonplaceholder.typicode.com/"
	user = requests.get(url + "users/{}".format(sys.argv[1])).json()
	todos = requests.get(url + "todos", params={"userId": sys.argv[1]}).json()
	USERNAME = user["username"]
	filename ="USER_ID"
	USER_ID = sys.argv[1]

	with open("{}.csv".format(filename), "w", newline="", encoding="utf-8") as f:
		write = csv.writer(f, quoting=csv.QUOTE_ALL)
		write.writerow(["USER_ID", "USERNAME", "COMPLETED", "TITLE"])  # Header row
        # write rows
		for task in todos:
			write.writerow([
				USER_ID,
				USERNAME,
				task.get("completed"),
				task.get("title")
			])
	
