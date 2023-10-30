import pytest
from main import Calculator

#
#Файл с тестами основного метода приложения
#
add_params = {
    "kafka":{
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0,
        "test": 0
    },

    "elasticsearch": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "processor": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "server": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "database_server": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "clickhouse": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "synchronizer": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "scanner": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    }   
}
incomplete_conf = {
    "kafka":{

    },

    "elasticsearch": {
        
    },
    "processor": {
        
    },
    "server": {
        
    },
    "database_server": {
       
    },
    "clickhouse": {
        
    },
    "synchronizer": {
       
    },
    "scanner": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    }   
}
incomplete_conf2 ={
    "elasticsearch": {
        
    },
    "processor": {
        
    },
    "server": {
        
    }
}
empty_conf = {}

test_no_change_add_params = {
    "kafka": {
        "replicas": 1,
        "memory": 100,
        "cpu": 5.92,
        "storage": 0.338,
        "test": 0
    },
    "elasticsearch": {
        "replicas": 1,
        "memory": 0,
        "cpu": 3,
        "storage": 0.256
    },
    "processor": {
        "replicas": 0,
        "memory": 100,
        "cpu": 3,
        "storage": -0.764
    },
    "server": {
        "replicas": 2,
        "memory": 100,
        "cpu": 1,
        "storage": 2.382
    },
    "database_server": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 3.959
    },
    "clickhouse": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 0
    },
    "synchronizer": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 0
    },
    "scanner": {
        "replicas": 1,
        "memory": 300,
        "cpu": 1,
        "storage": 0
    }
}
test_incomplete_conf = {
    "kafka": {
        "replicas": 1,
        "memory": 100,
        "cpu": 5.92,
        "storage": 0.338,
    },
    "elasticsearch": {
        "replicas": 1,
        "memory": 0,
        "cpu": 3,
        "storage": 0.256
    },
    "processor": {
        "replicas": 0,
        "memory": 100,
        "cpu": 3,
        "storage": -0.764
    },
    "server": {
        "replicas": 2,
        "memory": 100,
        "cpu": 1,
        "storage": 2.382
    },
    "database_server": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 3.959
    },
    "clickhouse": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 0
    },
    "synchronizer": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 0
    },
    "scanner": {
        "replicas": 1,
        "memory": 300,
        "cpu": 1,
        "storage": 0
    }
}
test_incomplete_conf2 = {
    "elasticsearch": {
        "replicas": 1,
        "memory": 0,
        "cpu": 3,
        "storage": 0.256
    },
    "processor": {
        "replicas": 0,
        "memory": 100,
        "cpu": 3,
        "storage": -0.764
    },
    "server": {
        "replicas": 2,
        "memory": 100,
        "cpu": 1,
        "storage": 2.382
    }
}
test_empty_conf = {}

full_configuration = {
    "kafka":{
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "elasticsearch": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0,
    },
    "processor": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "server": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "database_server": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "clickhouse": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "synchronizer": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    },
    "scanner": {
        "replicas": 0,
        "memory": 0,
        "cpu": 0,
        "storage": 0
    }   
}

test_calc_answer = {
    "kafka": {
        "replicas": 3,
        "memory": 1068.595755,
        "cpu": 5.04,
        "storage": 0.338
    },
    "elasticsearch": {
        "replicas": 3,
        "memory": 0,
        "cpu": 3,
        "storage": 0.256
    },
    "processor": {
        "replicas": 3,
        "memory": 953.6603,
        "cpu": 3,
        "storage": -0.737
    },
    "server": {
        "replicas": 2,
        "memory": 953.66,
        "cpu": 1,
        "storage": 2.384
    },
    "database_server": {
        "replicas": 1,
        "memory": 5233.374,
        "cpu": 1,
        "storage": 4.791
    },
    "clickhouse": {
        "replicas": 1,
        "memory": 5233.374,
        "cpu": 1,
        "storage": 0.64
    },
    "synchronizer": {
        "replicas": 1,
        "memory": 1.048,
        "cpu": 1,
        "storage": 0.608
    },
    "scanner": {
        "replicas": 1,
        "memory": 300,
        "cpu": 1,
        "storage": 0.608
    }
}
test_calc_answer2 = {
    "kafka": {
        "replicas": 1,
        "memory": 100,
        "cpu": 3.98,
        "storage": 0.333
    },
    "elasticsearch": {
        "replicas": 1,
        "memory": 0,
        "cpu": 3,
        "storage": 0.256
    },
    "processor": {
        "replicas": 0,
        "memory": 100,
        "cpu": 3,
        "storage": -1.177
    },
    "server": {
        "replicas": 2,
        "memory": 100,
        "cpu": 1,
        "storage": 2.36
    },
    "database_server": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 3.847
    },
    "clickhouse": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 0
    },
    "synchronizer": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 0
    },
    "scanner": {
        "replicas": 1,
        "memory": 300,
        "cpu": 1,
        "storage": 0
    }
}
test_calc_answer3 = {
    "kafka": {
        "replicas": 1,
        "memory": 100,
        "cpu": 5.63,
        "storage": 0.338
    },
    "elasticsearch": {
        "replicas": 1,
        "memory": 0,
        "cpu": 3,
        "storage": 0.256
    },
    "processor": {
        "replicas": 0,
        "memory": 100,
        "cpu": 3,
        "storage": -0.737
    },
    "server": {
        "replicas": 2,
        "memory": 100,
        "cpu": 1,
        "storage": 2.384
    },
    "database_server": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 4.287
    },
    "clickhouse": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 0
    },
    "synchronizer": {
        "replicas": 1,
        "memory": 100,
        "cpu": 1,
        "storage": 0
    },
    "scanner": {
        "replicas": 1,
        "memory": 300,
        "cpu": 1,
        "storage": 0
    }
}



@pytest.mark.parametrize('dic_config, agents, storage, traffic, \
                         mail_traffic, distributed, nodes, updated_config',[(add_params, 35, 1454.74436, 2042.87818, 3820.99851, False, 40, test_no_change_add_params),
                                                                            (incomplete_conf, 35, 1454.74436, 2042.87818, 3820.99851, False, 40, test_incomplete_conf),
                                                                            (incomplete_conf2, 35, 1454.74436, 2042.87818, 3820.99851, False, 40, test_incomplete_conf2),
                                                                            (empty_conf, 35, 1454.74436, 2042.87818, 3820.99851, False, 40, test_empty_conf),
                                                                            (full_configuration, 36, 3270.85901, 1907.3206, 2137.19151, True, 34, test_calc_answer),
                                                                            (full_configuration, 23, 3086.66144, 3191.79398, 1941.09035, False, 27, test_calc_answer2),
                                                                            (full_configuration, 36, 3933.57667, 3076.67716, 3820.99851, False, 38, test_calc_answer3)
                                                                            ])
def test_different_input_config(dic_config,agents, storage, traffic, mail_traffic, distributed, nodes, updated_config):
    calculator = Calculator(dic_config)
    assert calculator.update_config(agents, storage, traffic, mail_traffic, distributed, nodes) == updated_config
