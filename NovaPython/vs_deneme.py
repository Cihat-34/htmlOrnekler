import requests
url = "https://www.omdbapi.com/?i=tt3896198&apikey=4cde8281"
response = requests.get(url)
data = response.json()
print(data)