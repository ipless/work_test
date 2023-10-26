import pytest
import json
from main import Calculator
import testDir

with open('services.json') as f:
        config=json.load(f)

for x in range(5):
    name = 'input_data' + str(x)+'_test.json'
    calculator = Calculator(config)
    calculator = Calculator(config)
    inputData = help.checkRightInputData(name)
    updated_config = calculator.update_config(inputData['agents'], inputData['storage'], inputData['traffic'], 
                                              inputData['mail_traffic'], inputData['distributed'], inputData['nodes'])