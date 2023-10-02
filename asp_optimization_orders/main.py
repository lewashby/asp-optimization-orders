from clingo import Control
from dumbo_asp.primitives import Model
from utils import read_file, create_json_object, logger
from generator import Generator
from context import Context
import time


def main():
    # sample_input_facts = read_file("./sample_input.txt")
    ENCODING = read_file("./encoding.asp")
    control = Control(logger=logger)
    generator = Generator()
    facts = generator.generate_random_input(3,3)
    try:
        start_time = time.time()
        control.add(f"{facts}\n{ENCODING}")
        control.ground([("base", [])], context=Context())
        model = Model.of_control(control)
        res = model.as_facts.split('\n')
        print("Time: --- %s seconds ---" % (round(time.time() - start_time, 2)))
        res = filter(lambda x: x["quantity"] != 0, map(lambda y: create_json_object(y), res))
        res = list(res)
        print(res)
        print(generator.get_shippings_costs())
        print(generator.calculate_cost(res))

    except Exception as e:
        print(e)
        print([])

if __name__ == '__main__':
    main()