import copy
import json
import math

#так как в тз не сказано, что делать в случае, если на вход подается не полная конфигурация или пустой json файл,
#то программа будет генерировать конфигурация для всех сервисов, которые были приведены в задании 


class help:
    def roundUp(float_number:float, number_of_decimals:int):
        """ функция округления в большую сторону до определенного знака """
        return math.ceil(float_number*pow(10,number_of_decimals))/pow(10,number_of_decimals)
    
    def checkRightInputData(input_data:str) -> dict:
        """ функция для проверки корректрности входных типов данных"""
        with open(input_data) as f:
            buffer = json.load(f)
            if (isinstance(buffer['agents'], int) and isinstance(buffer['storage'], float) and
                isinstance(buffer['traffic'], float) and isinstance(buffer['mail_traffic'], float)
                and isinstance(buffer['distributed'], bool) and isinstance(buffer['nodes'], int)):
                return buffer
            else:
                raise Exception('incorrect input')
    
class Calculator:

    def __init__(self, config: dict):
        self._config = config

    def update_config(self, agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int) -> dict:
        """Функция для генерации конфигурации"""
        buffer = copy.deepcopy(self._config)
        

        buffer['kafka'] = buffer['kafka'] if 'kafka' in buffer else {}
        buffer['kafka']['replicas'] = 3 if distributed else 1
        buffer['kafka']['memory'] = mail_traffic*0.5 if distributed else 100
        buffer['kafka']['cpu'] = help.roundUp((0.000169*agents+0.437923)*nodes/3,2)
        buffer['kafka']['storage'] = help.roundUp(0.0004*agents+0.3231,3)
        
        buffer['elasticsearch'] = buffer['elasticsearch'] if 'elasticsearch' in buffer else {}
        buffer['elasticsearch']['replicas'] = 3 if distributed else 1
        buffer['elasticsearch']['memory'] = 0
        buffer['elasticsearch']['cpu'] = 3
        buffer['elasticsearch']['storage'] = 0.256 if agents<5000 else 0.512 if agents<10000 else 1
        
        buffer['processor'] = buffer['processor'] if 'processor' in buffer else {}
        buffer['processor']['replicas'] = (3 if distributed==1 else 0) if (agents>0 and storage>0) else 0
        buffer['processor']['memory'] = traffic*0.5 if distributed else 100
        buffer['processor']['cpu'] = 3
        buffer['processor']['storage'] = help.roundUp(-4.25877+0.98271*math.log(agents),3) if nodes>0 else 0
        
        buffer['server'] = buffer['server'] if 'server' in buffer else {}
        buffer['server']['replicas'] = min(agents,2) if (agents>0 and storage>0) else 0             
        buffer['server']['memory'] = round(traffic*0.5,3) if distributed else 100
        buffer['server']['cpu'] = 1
        buffer['server']['storage'] = help.roundUp((0.0019*agents+2,3154),3) if nodes>0 else 0
        
        buffer['database_server'] = buffer['database_server'] if 'database_server' in buffer else {}
        buffer['database_server']['replicas'] = (max(round(agents/15000,1)) if distributed else 1) if agents>0 else 0
        buffer['database_server']['memory'] = round(storage*1.6,3) if distributed else 100
        buffer['database_server']['cpu'] = 1
        buffer['database_server']['storage'] = help.roundUp((0.00000002*agents*agents+0.00067749*agents+4.5)*agents/nodes,3) if nodes>0 else 0
        
        buffer['clickhouse'] = buffer['clickhouse'] if 'clickhouse' in buffer else {}
        buffer['clickhouse']['replicas'] = (max(round(agents/15000),1) if distributed else 1) if agents>0 else 0 
        buffer['clickhouse']['memory'] = round(storage*1.6,3) if distributed else 100
        buffer['clickhouse']['cpu'] = 1
        buffer['clickhouse']['storage'] = help.roundUp(0.0000628*agents+0.6377,3) if distributed else 0
        
        buffer['synchronizer'] = buffer['synchronizer'] if 'synchronizer' in buffer else {}
        buffer['synchronizer']['replicas'] = 1 if agents>0 else 0
        buffer['synchronizer']['memory'] = help.roundUp(storage/5000,3)*1.6 if distributed else 100
        buffer['synchronizer']['cpu'] = 1
        buffer['synchronizer']['storage'] = help.roundUp(0.0002*agents+0.6,3) if distributed else 0
        
        buffer['scanner'] = buffer['scanner'] if 'scanner' in buffer else {}
        buffer['scanner']['replicas'] = 1 if agents>0 else 0
        buffer['scanner']['memory'] = 300 
        buffer['scanner']['cpu'] = 1
        buffer['scanner']['storage'] = help.roundUp(0.0002*agents+0.6,3) if distributed else 0
        
        return buffer

if __name__ == '__main__':
    
    config = None
    with open('services.json') as f:
        config=json.load(f)

    calculator = Calculator(config)
    inputData = help.checkRightInputData('inputData.json')
    
    updated_config = calculator.update_config(inputData['agents'], inputData['storage'], inputData['traffic'], 
                                              inputData['mail_traffic'], inputData['distributed'], inputData['nodes'])
    
    with open('updateCon.json', 'w') as f:
        json.dump(updated_config, f)