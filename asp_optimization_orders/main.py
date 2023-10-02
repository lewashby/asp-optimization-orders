from clingo import Control
from dumbo_asp.primitives import Model
from utils import read_file, create_json_object, logger
from generator import Generator
from context import Context
import time
import argparse
import random
from statistics import mean
from tqdm import tqdm

runs = 10

# Options
options = "hf:"

 # Long options
long_options = ["Help", "Facts"]

def main():

    parser=argparse.ArgumentParser(
        description='''Cart Optimization. ''',
        epilog="""Hope you get the best fit!!."""
    )
    parser.add_argument('--test', action='store_false', help='Run with random inputs', required=True)

    ENCODING = read_file("./encoding.asp")
    control = Control(logger=logger)
    generator = Generator()
    run_times = []
    for _ in tqdm(range(runs), desc="Testing..."):
        t_warehouses = random.randint(1, 10)
        t_products = random.randint(1, 10)
        facts = generator.generate_random_input(t_warehouses, t_products)
    
        try:
            start_time = time.time()
            control.add(f"{facts}\n{ENCODING}")
            control.ground([("base", [])], context=Context())
            model = Model.of_control(control)
            res = model.as_facts.split('\n')
            execution_time = round(time.time() - start_time, 2)
            run_times.append(execution_time)
            # res = filter(lambda x: x["quantity"] != 0, map(lambda y: create_json_object(y), res))
            # res = list(res)
            # print(res)
            # print(generator.get_shippings_costs())
            # print(generator.calculate_cost(res))

        except Exception:
            pass

    print(f"Mean execution time: {mean(run_times)}")

if __name__ == '__main__':
    main()