from minizinc import Instance, Model, Solver

class MinizincSolver:

    def __init__(self, encoding_path):
        model = Model(encoding_path)
        gecode = Solver.lookup("gecode")
        self.model = Instance(gecode, model)

    def solve(self, parameters: dict):
        for k in parameters.keys():
            self.model[k] = parameters[k]
        return self.model.solve()