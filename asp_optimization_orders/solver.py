from clingo import Control
from dumbo_asp.primitives import Model
from context import Context
from utils import read_file, parse_response, calculate_cost

def logger(code, msg):
    return

class Solver:

    def __init__(self, encoding_path):
        self.__encoding = read_file(encoding_path)
    

    def solve(self, facts, arguments=["--opt-strategy=usc,k,0,5" ,"--opt-usc-shrink=rgs"]):
        control = Control(arguments, logger=logger)
        control.add(f"{facts}\n{self.__encoding}")
        control.ground([("base", [])], context=Context())
        model = Model.of_control(control)
        result = model.as_facts.split('\n')
        return parse_response(result)
    
    @staticmethod
    def calculate_cost(result: list, p_prices: list, w_shipping_cost: list, w_threshold: list):
        return calculate_cost(result, p_prices, w_shipping_cost, w_threshold)