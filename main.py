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
        return math.ceil(float_number*pow(10,number_of_decimals))/pow(10,number_of_decimals)
    
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
                #
                #подумать по поводу ввода данных, ибо корректировать каждый раз json 
                #такое себе занятие 
                #
                if 'agents' and 'storage' and 'traffic' and 'mail_traffic' and 'distributed' and 'nodes' in buffer:
                    if (isinstance(buffer['agents'], int) and isinstance(buffer['storage'], float) and
                        isinstance(buffer['traffic'], float) and isinstance(buffer['mail_traffic'], float)
                        and isinstance(buffer['distributed'], bool) and isinstance(buffer['nodes'], int)):
                        return buffer
                    else:
                        print('incorrect input data, waiting\n'+ Rightdic)
                        #
                        #сделать вывод формата /ожидалось получить и пример json
                        #
                        sys.exit()
                        raise Exception('incorrect input')
                        help.check_right_input(input_data)
                else:
                    print('incorrect input data, waiting\n'+ Rightdic)
                    sys.exit() 
                    raise Exception('incorrect input')
                    help.check_right_input(input_data)
class Calculator:

    def __init__(self, config: dict):
        self._config = config

    def update_config(self, agents:int, storage:float, traffic:float, mail_traffic:float, distributed:bool, nodes:int) -> dict:
        """Функция для генерации конфигурации"""
        buffer = copy.deepcopy(self._config)
        for x in buffer:
            #
            #возможно надо будет поменять if else на case 
            #прочить условия задачи на используемую версию python
            #
            if x == 'kafka':
                #buffer['kafka'] = buffer['kafka'] if 'kafka' in buffer else {}
                buffer['kafka']['replicas'] = 3 if distributed else 1
                buffer['kafka']['memory'] = mail_traffic*0.5 if distributed else 100
                buffer['kafka']['cpu'] = help.round_up((0.000169*agents+0.437923)*nodes/3,2)
                buffer['kafka']['storage'] = help.round_up(0.0004*agents+0.3231,3)
            
            elif x == 'elasticsearch':
            #buffer['elasticsearch'] = buffer['elasticsearch'] if 'elasticsearch' in buffer else {}
                buffer['elasticsearch']['replicas'] = 3 if distributed else 1
                buffer['elasticsearch']['memory'] = 0
                buffer['elasticsearch']['cpu'] = 3
                buffer['elasticsearch']['storage'] = 0.256 if agents<5000 else 0.512 if agents<10000 else 1
            
            elif x == 'processor':    
            #buffer['processor'] = buffer['processor'] if 'processor' in buffer else {}
                buffer['processor']['replicas'] = (3 if distributed==1 else 0) if (agents>0 and storage>0) else 0
                buffer['processor']['memory'] = traffic*0.5 if distributed else 100
                buffer['processor']['cpu'] = 3
                buffer['processor']['storage'] = help.round_up(-4.25877+0.98271*math.log(agents),3) if nodes>0 else 0
            
            elif x == 'server':
            #buffer['server'] = buffer['server'] if 'server' in buffer else {}
                buffer['server']['replicas'] = min(agents,2) if (agents>0 and storage>0) else 0             
                buffer['server']['memory'] = help.math_round(traffic*0.5,3) if distributed else 100
                buffer['server']['cpu'] = 1
                buffer['server']['storage'] = help.round_up((0.0019*agents+2,3154),3) if nodes>0 else 0

            elif x == 'database_server':    
            #buffer['database_server'] = buffer['database_server'] if 'database_server' in buffer else {}
                buffer['database_server']['replicas'] = (max(help.math_round(agents/15000,1)) if distributed else 1) if agents>0 else 0
                buffer['database_server']['memory'] = help.math_round(storage*1.6,3) if distributed else 100
                buffer['database_server']['cpu'] = 1
                buffer['database_server']['storage'] = help.round_up((0.00000002*agents*agents+0.00067749*agents+4.5)*agents/nodes,3) if nodes>0 else 0

            elif x == 'clickhouse':    
            #buffer['clickhouse'] = buffer['clickhouse'] if 'clickhouse' in buffer else {}
                buffer['clickhouse']['replicas'] = (max(help.math_round(agents/15000),1) if distributed else 1) if agents>0 else 0 
                buffer['clickhouse']['memory'] = help.math_round(storage*1.6,3) if distributed else 100
                buffer['clickhouse']['cpu'] = 1
                buffer['clickhouse']['storage'] = help.round_up(0.0000628*agents+0.6377,3) if distributed else 0

            elif x == 'synchronizer':    
            #buffer['synchronizer'] = buffer['synchronizer'] if 'synchronizer' in buffer else {}
                buffer['synchronizer']['replicas'] = 1 if agents>0 else 0
                buffer['synchronizer']['memory'] = help.round_up(storage/5000,3)*1.6 if distributed else 100
                buffer['synchronizer']['cpu'] = 1
                buffer['synchronizer']['storage'] = help.round_up(0.0002*agents+0.6,3) if distributed else 0

            elif x == 'scanner':   
            #buffer['scanner'] = buffer['scanner'] if 'scanner' in buffer else {}
                buffer['scanner']['replicas'] = 1 if agents>0 else 0
                buffer['scanner']['memory'] = 300 
                buffer['scanner']['cpu'] = 1
                buffer['scanner']['storage'] = help.round_up(0.0002*agents+0.6,3) if distributed else 0
            
        return buffer

if __name__ == '__main__':
    
    config = None
    config=help.check_none_json('testServices.json')

    calculator = Calculator(config)
    inputData = help.check_right_input('inputData.json')
    
    updated_config = calculator.update_config(inputData['agents'], inputData['storage'], inputData['traffic'], 
                                              inputData['mail_traffic'], inputData['distributed'], inputData['nodes'])
    
    with open('updateCon.json', 'w') as f:
        json.dump(updated_config, f)