from clingo import Control
from dumbo_asp.primitives.models import Model
from context import Context
from utils import read_file, parse_response, calculate_cost

def logger(code, msg):
    return

class Solver:

    def __init__(self, encoding_path):
        self.__encoding = read_file(encoding_path)
    
    

    def solve(self, facts, arguments=["--opt-strategy=usc,k,0,5" ,"--opt-usc-shrink=rgs"], timeout=2):

        results: list = []
        handle = None
        def on_model(m):
            results.append(Model.of_atoms(m.symbols(shown=True)))
        
        control = Control(arguments, logger=logger)
        control.add(f"{facts}\n{self.__encoding}")
        control.ground([("base", [])], context=Context())

        with control.solve(on_model=on_model, async_=True) as handle:
            handle.wait(timeout)
            handle.cancel()
            handle = handle.get()
            
        model = results[0] if len(results) > 0 else Model.empty()
        result = model.as_facts.split('\n') if len(model) > 0 else []
        
        return parse_response(result), handle.interrupted, handle.satisfiable
    
    @staticmethod
    def calculate_cost(result: list, p_prices: list, w_shipping_cost: list, w_threshold: list):
        return calculate_cost(result, p_prices, w_shipping_cost, w_threshold)