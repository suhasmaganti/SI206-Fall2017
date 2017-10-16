import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ')
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve all of the anchor tags
tags = soup('a')

count = int(input('Enter count: '))
pos = int(input('Enter position: '))

def fcount(url):
	names = []
	html = urllib.request.urlopen(url, context=ctx).read()
	soup = BeautifulSoup(html, 'html.parser')
	tags = soup('a')
	for tag in tags:
		names.append(tag.get('href', None))
	return names[pos-1]

for i in range(count+1):
	print('Retrieving: ', url)
	url = fcount(url)