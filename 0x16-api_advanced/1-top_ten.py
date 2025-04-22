#!/usr/bin/python3
"""
1-top_ten module
"""
import requests
def top_ten(subreddit):
	""" Returns the top ten titles for the hot posts"""
	url=f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
	headers={"User-Agent":"My-User-Agent"}
	response=requests.get(url, headers=headers, allow_redirects=False)
	if response.status_code== 200:
		data=response.json()
		posts = data.get("data", {}).get("children", [])
		for post in posts:
			print(post["data"]["title"])
	else:
		print(None)

	
