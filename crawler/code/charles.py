import requests

proxies = {
    "http": "localhost:8888",
    "https": "localhost:8888",
}
resp = requests.get('http://xkcd.com', proxies=proxies)
print(resp.text)
