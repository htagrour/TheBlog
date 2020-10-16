import requests, json

data = json.dumps({'body':'hello world1'})
res = requests.post('http://127.0.0.1:5000/',data, auth = ('hamza', '1234'))
print(res.text)