from pylistic import Pylistic

def test_find():
    my_list_of_dict = [
        {
            'a': 2,
            'b': 2
        },
        {
            'a': 2,
            'b': 3
        },
        {
            'a': 3,
            'b': 4
        }
    ]
    
    pylist = Pylistic(my_list_of_dict) 
    
    index_of_item = pylist.find_first('a', 2)
    assert index_of_item == 0
    
    index_of_item = pylist.find('a', 2)
    assert index_of_item == 0
    
    index_of_item = pylist.find('a', 2, amount=3)
    assert index_of_item == [0, 1]
    
    index_of_item = pylist.find('a', 2, max=True)
    assert index_of_item == [0, 1]
    
    index_of_item = pylist.find_all('a', 2)
    assert index_of_item == [0, 1]

def test_find2():
    test_obj = [
        {
            'reports': [
                {
                    'node': 'a',
                    'revenue': 1,
                    'unloaded': 0
                },
                {   'node_name': 'b',
                    'revenue': 1,
                    'unloaded': 0
                },
                {   'node_name': 'c',
                    'revenue': 1,
                    'unloaded': 0
                }
            ]
        },
        {
            'reports': [
                {   'node_name': 'a',
                    'revenue': 10,
                    'unloaded': 5
                },
                {   'node': 'b',
                    'revenue': 1,
                    'unloaded': 2
                },
                {   'node_name': 'c',
                    'revenue': 3,
                    'unloaded': 2
                }
            ]
        }
    ]
    
    pylist = Pylistic(test_obj)
    reports = pylist.loop_over('reports', 'node')
    expected_result = [
        {
            'node': 'a',
            'revenue': 1,
            'unloaded': 0
        },
        {   
            'node': 'b',
            'revenue': 1,
            'unloaded': 2
        }
    ]
    assert reports == expected_result
    
    node_a = pylist.loop_over('reports', 'node', 'a')
    expected_result = [
        {
            'node': 'a',
            'revenue': 1,
            'unloaded': 0
        }
    ]
    assert node_a == expected_result