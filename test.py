#! /usr/bin/env python

import sys
import os
import requests

tikaServerURL = 'http://localhost:9998/'
epub = '/media/johan/Elements1/ebooks-test/testsmall/epub20_minimal.epub'

url = tikaServerURL + 'tika'
payload = open(os.path.normpath(epub), "rb")
#payload = "bla bla bla"

#with open(os.path.normpath(epub), "rb") as f:
#    payload = f.read(1)

print(type(payload))
headers = {'Accept': 'text/plain'}
headers = {'Content-type': 'application/epub+zip'}

# curl -X PUT --data-binary @GeoSPARQL.pdf http://localhost:9998/tika --header "Content-type: application/pdf"

#r = requests.post(url, data=payload, headers=headers)
r = requests.put(url, data=payload, headers=headers)
print(r.encoding)
#print(r.content)
print(r.text)
