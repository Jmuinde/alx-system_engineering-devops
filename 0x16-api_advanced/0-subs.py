#!/usr/bin/python3
"""
Script to get the number of subscribers for a 
given subreddit
"""
import requests


def number_of_subscribers(subreddit):
	url =f"https://www.reddit.com/r/{subreddit}/about.json"
	headers={"User-Agent": "My-User-Agent"} 
	response = requests.get(url, headers=headers, allow_redirects=False)
	if response.status_code == 200:
		data=response.json()
		return data["data"].get("subscribers", 0)
	else:
		return 0


