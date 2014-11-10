#!/usr/bin/env python3
fi = open('googledata.json','r')
a = fi.read()
import json
b = json.loads(a)['items']
print (b[56])
