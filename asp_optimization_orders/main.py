from generator import Generator
import time
import argparse
import random
from statistics import mean
from tqdm import tqdm
from greedy import Greedy
from solver import Solver
import sys
import random

max_warehouses = 20
max_products = 20

def sample():
    solver = Solver("./encoding.asp")
    generator = Generator()
    t_warehouses = 4
    t_products = 4
    facts, p_prices, p_requests, w_shipping_costs, w_free_shipping, s_matrix = generator.generate_random_input(t_warehouses, t_products)

    print(f"products requirements: {p_requests}")
    print(f"products prices: {p_prices}")
    print(f"warehouses shippings cost: {w_shipping_costs}")
    print(f"warehouses free shipping threshold: {w_free_shipping}")
    print()

    p_requirements = [(i+1, r) for i, r in enumerate(p_requests)]
    greedy = Greedy(t_warehouses, p_requirements, p_prices, w_shipping_costs, w_free_shipping, s_matrix)
    allocations = greedy.allocate_items()
    cost, count = greedy.calculate_costs(allocations)
    print("Greedy solution")
    print(allocations)
    print(f"Shippings created: {count}")
    print(f"Total shipping cost: {cost}")
    print()

    result = solver.solve(facts)
    cost, count = solver.calculate_cost(result, p_prices, w_shipping_costs, w_free_shipping)
    print("ASP solution")
    print(result)
    print(f"Shippings created: {count}")
    print(f"Total shipping cost: {cost}")

def main():

    parser=argparse.ArgumentParser(
        description='''Cart Optimization. ''',
        epilog="""Hope you get the best fit!!."""
    )
    parser.add_argument('--test', action='store_true', help='Run with random inputs', required='--one-time' not in sys.argv)
    parser.add_argument('-r', nargs=1, help='Max amount of runs', type=int,  required='--test' in sys.argv)
    parser.add_argument('--one-time', action='store_true', help='One sample comparison test')
    parser.add_argument('-s', nargs=1, type=int, help='Seed for random generation')
    args=parser.parse_args()
    if (args.s):
        random.seed(args.s[0])
    if (args.one_time == True):
        sample()
        return

    max_runs=args.r[0]

    solver = Solver("./encoding.asp")
    generator = Generator()
    asp_run_times = []
    greedy_run_times = []
    total_asp_cost = 0
    total_asp_count = 0
    total_greedy_cost = 0
    total_greedy_count = 0
    
    for _ in tqdm(range(max_runs), desc="Testing..."):
        t_warehouses = random.randint(1, max_warehouses)
        t_products = random.randint(1, max_products)
        facts, p_prices, p_requests, w_shipping_costs, w_free_shipping, s_matrix = generator.generate_random_input(t_warehouses, t_products)
        p_requirements = [(i+1, r) for i, r in enumerate(p_requests)]
        greedy = Greedy(t_warehouses, p_requirements, p_prices, w_shipping_costs, w_free_shipping, s_matrix)
        try:
            start_time_asp = time.time()
            asp_result = solver.solve(facts)
            execution_time = round(time.time() - start_time_asp, 2)
            asp_run_times.append(execution_time)

            asp_cost, asp_count = solver.calculate_cost(asp_result, p_prices, w_shipping_costs, w_free_shipping)
            total_asp_cost += asp_cost
            total_asp_count += asp_count

            start_time_greedy = time.time()
            greedy_result = greedy.allocate_items()
            execution_time = round(time.time() - start_time_greedy, 2)
            greedy_run_times.append(execution_time)
            greedy_cost, greedy_count = greedy.calculate_costs(greedy_result)
            total_greedy_cost += greedy_cost
            total_greedy_count += greedy_count

        except Exception as e:
            pass

    if len(asp_run_times) > 0:
        print(f"Solutions found: {len(asp_run_times)}")
        print(f"Mean ASP execution time: {round(mean(asp_run_times),2)}")
        print(f"Total ASP Shippings created: {total_asp_count}")
        print(f"Total ASP cost: {total_asp_cost}")
        print(f"Mean Greedy execution time: {round(mean(greedy_run_times),2)}")
        print(f"Total Greedy Shippings created: {total_greedy_count}")
        print(f"Total Greedy cost: {total_greedy_cost}")
    else:
        print("No solutions found")

if __name__ == '__main__':
    main()