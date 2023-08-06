from pylistic import DictList
from pylistic import ListList

class Pylistic:
    
    def __init__(self, list: list=[]):
        self.pylist = list
        self.__set_type()
        
    def __set_type(self):
        types = {
            'dict': DictList(self.pylist),
            'list': ListList(self.pylist)
        }
        self.type = None
        if self.pylist:
            self.type = types[type(self.pylist[0]).__name__]

    def add(self, list_data):
        self.pylist = list_data
    
    def append(self, item):
        self.pylist.append(item)
    
    def pop(self):
        self.pylist.pop()
    
    def find_first(self, key, item=None):
        try:
            for data in self.pylist:
                if data[key] == item or (data[key] and item==None):
                    return self.pylist.index(data)
            return None
        except KeyError:
            print(f'ERROR. Key {key} not found')
            raise

    def find_all(self, key, item=None):
        try:
            list_of_indexes = []
            for data in self.pylist:
                if data[key] == item or (data[key] and item==None):
                    list_of_indexes.append(self.pylist.index(data))
            return list_of_indexes
        except KeyError:
            print(f'ERROR. Key {key} not found')
            raise
    
    def find(self, key, item=None, amount:int=1, max=False):
        if amount == 1 and not max:
            return self.find_first(key, item)
        if max:
            amount = len(self.pylist)      
        list_of_indexes = []
        for data in self.pylist:
            if (data[key] == item and len(list_of_indexes)<amount) or (data[key] and item==None):
                list_of_indexes.append(self.pylist.index(data)) 
        return list_of_indexes
    
    def loop_over(self, outter_key: str, inner_key: str, value=None):
        try:
            if isinstance(self.type, DictList):
                return self.type.loop_over(outter_key, inner_key, value)
        except TypeError:
            print('Object must be a Pylistict DictList')
            raise
        
    def __repr__(self) -> str:
        msg_str = 'Pylistic '
        if self.type:
            msg_str += type(self.type).__name__
        return msg_str