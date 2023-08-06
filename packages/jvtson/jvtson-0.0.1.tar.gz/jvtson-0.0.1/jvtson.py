import json

class Jvt():
    def initjvt(self, name : str):
        with open(name) as file:
            global stock
            stock = json.load(file)
            return stock

    def readjvt(self, name : str, subname : str):
        for i in stock[subname]:
            res = i[name]
            return res

    def writejvt(self, name : str, onjson, indent : int):
        with open(name, 'w') as file:
            json.dump(onjson, file, indent=indent)
    
    def normalizejvt(self, name, indent : int):
        res = json.dumps(name, indent=indent)
        return res

    def delizejvt(self, name):
        res = json.loads(name)
        return res