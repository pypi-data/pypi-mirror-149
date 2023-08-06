from typing import Tuple
# from pylistic.pylistic import Pylistic

class DictList():
    def __init__(self, pylist):
        self.pylist = pylist

    def __loop_over_with_value(self, outter_key, inner_key, value) -> list:
        list_of_dicts = []
        for item in self.pylist:
            dict_data = item.get(outter_key, [])
            list_of_dicts.extend(
                list(filter(lambda data:data.get(inner_key)==value, dict_data))
            )
        return list_of_dicts
    
    def __loop_over_with_key(self, outter_key, inner_key) -> list:
        list_of_dicts = []
        for item in self.pylist:
            dict_data = item.get(outter_key, [])
            list_of_dicts.extend(
                list(filter(lambda data:data.get(inner_key), dict_data))
            )
        return list_of_dicts

    def loop_over(self, outter_key: str, inner_key: str, value=None) -> list:
        if value is not None:
            list_of_dicts = self.__loop_over_with_value(outter_key=outter_key, inner_key=inner_key, value=value)
        else:
            list_of_dicts = self.__loop_over_with_key(outter_key=outter_key, inner_key=inner_key)
        return list_of_dicts
    
    def __repr__(self) -> str:
        return 'Pylistic -> Dict List'