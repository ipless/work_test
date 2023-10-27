
import json
from main import Calculator
import testDir

with open('services.json') as f:
        config=json.load(f)

for x in config:
        print(x)