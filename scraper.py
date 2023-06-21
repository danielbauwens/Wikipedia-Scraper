import requests

url = "https://country-leaders.onrender.com/status"
r = requests.get(url)
print(r, status_code)