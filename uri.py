import urllib.request
import json

url = 'http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitle&title=canada'
r = urllib.request.urlopen(url)
data = json.load(r)
print(data)