#!/usr/bin/python3
"""Fethes employe's data from the provided url"""
import requests
import sys

if __name__ == "__main__":
	url = "https://jsonplaceholder.typicode.com/"
	user = requests.get(url + "users/{}".format(sys.argv[1])).json()
	work = requests.get(url + "todos", params={"userId":sys.argv[1]}).json()
	name = user["name"]
	complete = [t.get('title') for t in work if t.get('completed') is True]
	print("Employee {} is done with tasks({}/{}):".format(name, len(complete),
															len(work)))
	[print("\t {}".format(c)) for c in complete]
	# print(user)

