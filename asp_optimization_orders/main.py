from clingo import Control
from dumbo_asp.primitives import Model
from utils import read_file, logger
from generator import Generator
from context import Context
import time
import argparse
import random
from statistics import mean
from tqdm import tqdm

max_warehouses = 10
max_products = 10

def main():

    parser=argparse.ArgumentParser(
        description='''Cart Optimization. ''',
        epilog="""Hope you get the best fit!!."""
    )
    parser.add_argument('--test', action='store_true', help='Run with random inputs', required=True)
    parser.add_argument('-r', nargs=1, help='Max amount of runs', type=int, required=True)
    args=parser.parse_args()
    max_runs=args.r[0]

    ENCODING = read_file("./encoding.asp")
    generator = Generator()
    run_times = []
    for _ in tqdm(range(max_runs), desc="Testing..."):
        t_warehouses = random.randint(1, max_warehouses)
        t_products = random.randint(1, max_products)
        facts = generator.generate_random_input(t_warehouses, t_products)
    
        try:
            control = Control(logger=logger)
            start_time = time.time()
            control.add(f"{facts}\n{ENCODING}")
            control.ground([("base", [])], context=Context())
            model = Model.of_control(control)
            _ = model.as_facts.split('\n')
            execution_time = round(time.time() - start_time, 2)
            run_times.append(execution_time)

        except Exception as e:
            pass

    if len(run_times) > 0:
        print(f"Solutions found: {len(run_times)}")
        print(f"Mean execution time: {mean(run_times)}")
    else:
        print("No solutions found")

if __name__ == '__main__':
    main()