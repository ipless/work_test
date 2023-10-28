import copy
import json
import math
import sys

#
#Основные условия работы приложения:
#1. Все файлы должны лежать в дириктории с приложением
#2. название файла с передаваемыми параметрами "input_data.json"
#3. название файла с входной конфигурацией "servicesConf.json"
#4. реализовано на версии python 3.10+
#

#
#так как в тз не сказано, что делать в случае, если на вход подается не полная конфигурация или пустой json файл,
#то программа будет генерировать конфигурация для всех сервисов, которые были приведены в задании 
#входные данные будут передаваться через json, так как часто в этом формате собираются разные метрики с ПК
#само приложение будет консольным, так как от пользователя не требуется вводить что-либо в приложение
#
#git

class help:
    def math_round(float_number:float, number_of_decimals:int):
        """Математическое округление"""
        #написал собственный метод, ибо round() в python периодически выводит не правильное округление
        bufferNum = float_number*pow(10,number_of_decimals+1)
        return math.ceil(bufferNum/10)/pow(10,number_of_decimals) if bufferNum%10>=5 else math.floor(bufferNum/10)/pow(10,number_of_decimals)

        
    def round_up(float_number:float, number_of_decimals:int):
        """ функция округления в большую сторону до определенного знака """
        return math.ceil(float_number*pow(10, number_of_decimals))/pow(10, number_of_decimals)
    
    def check_none_json(filename: str):
        """проверка на пустой json"""
        try:
            with open(filename) as f:
                config=json.load(f)
                return config
        except:
            print('incorrect json file or not json file')
            sys.exit()

    def check_right_input(input_data:str) -> dict:
        """ функция для проверки корректрности входных типов данных"""

        #Строка с примером того, ято обязан содержать json файл
        Rightdic = "\"agents\": int, \n\"storage\": int \n\"traffic\": float, \
        \n\"traffic\": float, \n\"mail_traffic\": float, \n\"distributed\": bool,\
        \n\"nodes\": int "
                 
        
        incorrectFlag=True
        while incorrectFlag:
            with open(input_data) as f:
                buffer = json.load(f)
                #первое условие проверяет наличие всех входных переменных в json файле
                #второе условие проверяет правильность типов данных
                #в случае false выведет сообщение о некорректности данных и выйдет из приложения
                if 'agents' and 'storage' and 'traffic' and 'mail_traffic' and 'distributed' and 'nodes' in buffer:
                    if (isinstance(buffer['agents'], int) and isinstance(buffer['storage'], float) and
                        isinstance(buffer['traffic'], float) and isinstance(buffer['mail_traffic'], float)
                        and isinstance(buffer['distributed'], bool) and isinstance(buffer['nodes'], int)):
                        return buffer
                    else:
                        print('incorrect input data, waiting\n'+ Rightdic)
                        sys.exit()
                else:
                    print('incorrect input data, waiting\n'+ Rightdic)
                    sys.exit() 

class help_with_calc:
    """Данный класс содержит методы для расчета конфигурации сервисов"""
    def calc_kafka(agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int) -> dict:
        replicas = 3 if distributed else 1
        memory = mail_traffic*0.5 if distributed else 100
        cpu = help.round_up((0.000169*agents+0.437923)*nodes/3,2)
        storage = help.round_up(0.0004*agents+0.3231,3)
        return {
                'replicas':replicas,
                'memory':memory,
                'cpu':cpu,
                'storage':storage,
            }
    def calc_elasticsearch(agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int)-> dict:
        replicas = 3 if distributed else 1
        memory = 0
        cpu = 3
        storage = 0.256 if agents<5000 else 0.512 if agents<10000 else 1
        return {
            'replicas':replicas,
            'memory':memory,
            'cpu':cpu,
            'storage':storage,
            }
    def calc_processor(agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int)-> dict:
        replicas = (3 if distributed==1 else 0) if (agents>0 and storage>0) else 0
        memory = traffic*0.5 if distributed else 100
        cpu = 3
        storage = help.round_up(-4.25877+0.98271*math.log(agents),3) if nodes>0 else 0
        return {
            'replicas':replicas,
            'memory':memory,
            'cpu':cpu,
            'storage':storage,
            }
    def calc_server(agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int)-> dict:
        replicas = min(agents,2) if (agents>0 and storage>0) else 0             
        memory = help.math_round(traffic*0.5,3) if distributed else 100
        cpu = 1
        storage = help.round_up((0.0019*agents+2.3154),3) if nodes>0 else 0
        return {
            'replicas':replicas,
            'memory':memory,
            'cpu':cpu,
            'storage':storage,
            }
    def calc_database_server(agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int)-> dict:
        replicas = (max(help.math_round(agents/15000,1)) if distributed else 1) if agents>0 else 0
        memory = help.math_round(storage*1.6,3) if distributed else 100
        cpu = 1
        storage = help.round_up((0.00000002*agents*agents+0.00067749*agents+4.5)*agents/nodes,3) if nodes>0 else 0
        return {
                'replicas':replicas,
                'memory':memory,
                'cpu':cpu,
                'storage':storage,
            }
    def calc_clickhouse(agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int)-> dict:
        replicas = (max(help.math_round(agents/15000),1) if distributed else 1) if agents>0 else 0 
        memory = help.math_round(storage*1.6,3) if distributed else 100
        cpu = 1
        storage = help.round_up(0.0000628*agents+0.6377,3) if distributed else 0
        return {
                'replicas':replicas,
                'memory':memory,
                'cpu':cpu,
                'storage':storage,
            }
    def calc_synchronizer(agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int)-> dict:
        replicas = 1 if agents>0 else 0
        memory = help.round_up(storage/5000,3)*1.6 if distributed else 100
        cpu = 1
        storage = help.round_up(0.0002*agents+0.6,3) if distributed else 0
        return {
                'replicas':replicas,
                'memory':memory,
                'cpu':cpu,
                'storage':storage,
            }
    def calc_scanner(agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int)-> dict:
        replicas = 1 if agents>0 else 0
        memory = 300 
        cpu = 1
        storage = help.round_up(0.0002*agents+0.6,3) if distributed else 0
        return {
                'replicas':replicas,
                'memory':memory,
                'cpu':cpu,
                'storage':storage,
            }
class Calculator:

    def __init__(self, config:dict):
        self._config = config

    def update_config(self, agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int) -> dict:
        """Метод для генерации конфигурации"""
        dict_func = {   #словарь методов расчета конфигурации
            'kafka':help_with_calc.calc_kafka,
            'elasticsearch':help_with_calc.calc_elasticsearch,
            'processor':help_with_calc.calc_processor,
            'server':help_with_calc.calc_server,
            'database_server':help_with_calc.calc_database_server,
            'clickhouse':help_with_calc.calc_clickhouse,
            'synchronizer':help_with_calc.calc_synchronizer,
            'scanner':help_with_calc.calc_scanner
        }
        for service in self._config:
            for param in dict_func[service](agents, storage, traffic, mail_traffic, distributed, nodes):
                self._config[service][param]=dict_func[service](agents, storage, traffic, mail_traffic, distributed, nodes)[param]
        return  self._config
 
if __name__ == '__main__':
    
    config = None
    config=help.check_none_json('updateCon.json')

    calculator = Calculator(config)
    inputData = help.check_right_input('inputData.json')
    
    updated_config = calculator.update_config(inputData['agents'], inputData['storage'], inputData['traffic'], 
                                              inputData['mail_traffic'], inputData['distributed'], inputData['nodes'])
    
    with open('updateCon.json', 'w') as f:
        json.dump(updated_config, f)