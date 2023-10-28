
import json
from main import Calculator
import testDir



def kafka(a,b):
    return a+b
def serp(a,b):
    return a/b
def qwe(a,b):
    return a*b
def asd(a,b):
    return a-b
a=10
b=2
dicfunc={
    'kafka':kafka,
    'serp':serp,
    'qwe':qwe,
    'asd':asd
}
config = None
with open('testServices.json') as f:
     config=json.load(f)

for service in config:
    print(dicfunc[service](a,b))
