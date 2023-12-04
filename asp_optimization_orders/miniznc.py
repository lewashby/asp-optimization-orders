from minizinc import Instance, Model, Solver
from utils import calculate_cost

class MinizincSolver:

    def __init__(self, encoding_path, solver="gecode"):
        model = Model(encoding_path)
        gecode = Solver.lookup(solver)
        self.model = Instance(gecode, model)

    def solve(self, parameters: dict):
        for k in parameters.keys():
            self.model[k] = parameters[k]
        return self.model.solve()
    
    @staticmethod
    def parse_solution(result):
        if (result.solution is not None):
            solution = result.solution
            res = []
            for i, p in enumerate(solution.select):
                res += [{"warehouse": j+1, "product": i+1, "quantity": w } for j, w in enumerate(p) if w != 0]
            return {"objective": result.objective, "solution": res}
        return None
    
    @staticmethod
    def calculate_cost(result: list, p_prices: list, w_shipping_cost: list, w_threshold: list):
        return calculate_cost(result, p_prices, w_shipping_cost, w_threshold)
