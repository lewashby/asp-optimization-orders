from clingo import Control
from dumbo_asp.primitives import Model
from context import Context
from utils import read_file, parse_response
from functools import reduce

def logger(code, msg):
    return

class Solver:

    def __init__(self, encoding_path):
        self.__encoding = read_file(encoding_path)
    

    def solve(self, facts):
        control = Control(["--opt-strategy=usc,k,0,5" ,"--opt-usc-shrink=rgs"], logger=logger)
        control.add(f"{facts}\n{self.__encoding}")
        control.ground([("base", [])], context=Context())
        model = Model.of_control(control)
        result = model.as_facts.split('\n')
        return parse_response(result)
    
    @staticmethod
    def calculate_cost(result: list, p_prices: list, w_shipping_cost: list, w_threshold: list):
        total = 0
        count = 0
        for i, cost in enumerate(w_shipping_cost):
            index = i+1
            warehouse_allocations = list(filter(lambda x: x['warehouse'] == index, result))
            if (len(warehouse_allocations) > 0):
                count += 1
                spent = reduce(lambda sum, x: sum + x['quantity']*p_prices[x['product']-1], warehouse_allocations, 0)
                if spent >= w_threshold[i]:
                    cost = 0
                total+=cost
        return total, count