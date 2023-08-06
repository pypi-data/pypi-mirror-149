from .wrapper import Wrapper

class MappedDict:
    path = []
    content = {}

    def __init__(self, content: dict):
        self.content = content

    def dig_into(self, looking_for: str, offset = 0):
        def __dig_into(target: dict, looking_for: str, offset):
            for key in target.keys():
                if str(key) == str(looking_for):
                    if offset == 0:
                        return target
                    offset -= 1
                elif type(target[key]) is dict or type(target[key]) is Wrapper:
                    self.path.append(key)
                    return __dig_into(target[key], looking_for, offset)
            return {}
        return __dig_into(self.content, looking_for, offset)

    def resolve(self, ):
        def __resolve(target: dict, i = 0):
            i += 1
            if i > len(self.path):
                return target
            return __resolve(target[self.path[i - 1]], i)
        return __resolve(self.content)
    
    def get_path(self, ):
        return self.path.copy()

    def explore_path(self, index, value):
        if type(index) is str:
            for way_i in range(len(self.path)):
                if str(self.path[way_i]) == index:
                    res = self.get_path()
                    res[way_i] = value
                    return res
            return []
        res = self.get_path()
        if len(res) < index:
            res[index] = value
            return res
        return []
    
    def travel(self, index, value):
        content = self.content
        for step in self.explore_path(index, value):
            content = content.get(step, {})
        return content

    def find_step_pos(self, index):
        if type(index) is str:
            for way_i in range(len(self.path)):
                if str(self.path[way_i]) == index:
                    res = self.get_path()
                    res[way_i] = value
                    return way_i
        return None

    def get_total_of(self, index: str):
        res = 0
        i = 0
        while True:
            n = self.dig_into(index, i).get(index, None)
            i += 1
            if n is None:
                break
            res += n
        return res
    
    def get_total_prod_of(self, index1: str, index2: str):
        res = 0
        i = 0
        while True:
            s1 = self.dig_into(index1, i).get(index1, None)
            s2 = self.dig_into(index2, i).get(index2, None)
            i += 1
            if s1 is None or s2 is None:
                break
            res += s1 * s2
        return res
    
    def get_all_operated(self, *indexs: str, oper_func, ret_func=None):
        res = 0
        i = 0
        while True:
            ss = []
            for index in indexs:
                ss.append(self.dig_into(index, i).get(index, None))
            i += 1
            if ss.count(None) == len(ss):
                break
            ss.insert(0, res)
            res = oper_func(ss)
        if oper_func is not None:
            res = ret_func(res, i)
        return res

    def get(self, ):
        return self.content

