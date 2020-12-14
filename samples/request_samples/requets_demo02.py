import requests

session = requests.session()
response = session.get(url='http://www.hnxmxit.com/')
response.encoding = response.apparent_encoding
print(response.text)


