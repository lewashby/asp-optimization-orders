from generator import Generator
import time
import argparse
import random
from statistics import mean
from tqdm import tqdm
from greedy import Greedy
from solver import Solver
from miniznc import MinizincSolver
import sys
import random
import csv
import enum
import warnings

warnings.filterwarnings("error")

max_warehouses = 20
max_products = 20
timeout = 3.0

def sample_mnznc():
    model = MinizincSolver("./encodings/marketplace-1.mzn", solver="com.google.ortools.sat")
    generator = Generator()
    t_warehouses = 3
    t_products = 2
    _, p_prices, p_requests, w_shipping_costs, w_free_shipping, s_matrix = generator.generate_random_input(t_warehouses, t_products)

    print(f"products requirements: {p_requests}")
    print(f"products prices: {p_prices}")
    print(f"warehouses shippings cost: {w_shipping_costs}")
    print(f"warehouses free shipping threshold: {w_free_shipping}")
    print()

    ws = enum.Enum("warehouses", [f"w{i+1}" for i in range(t_warehouses)])
    ps = enum.Enum("products", [f"p{i+1}" for i in range(t_products)])    
    parameters: dict = {}
    parameters["products"] = ps
    parameters["warehouses"] = ws
    parameters["product_in_warehouse"] = s_matrix
    parameters["product_request"] = p_requests
    parameters["product_price"] = p_prices
    parameters["shipping_free_threshold"] = w_free_shipping
    parameters["shipping_fee"] = w_shipping_costs
    parameters["shipment_cost"] = 0
    parameters["used_warehouses"] = 1

    result = model.solve(parameters)
    result = model.parse_solution(result)

    if (result is None):
        print("No solution found")
    else:
        mnznc_cost, mnznc_count, mnznc_allocations_count = model.calculate_cost(result['solution'], p_prices, w_shipping_costs, w_free_shipping)
        
        print("Minizinc solution")
        print(result['solution'])
        print(f"Shippings created: {mnznc_count}")
        print(f"Total shipping cost: {mnznc_cost}")
        print(f"Total allocations created: {mnznc_allocations_count}")


def sample():
    solver = Solver("./encodings/encoding2.asp")
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
    cost, count, allocations_count = greedy.calculate_costs(allocations)
    print("Greedy solution")
    print(allocations)
    print(f"Shippings created: {count}")
    print(f"Total shipping cost: {cost}")
    print(f"Total allocations created: {allocations_count}")
    print()

    result, _, _ = solver.solve(facts)
    cost, count, allocations_count = solver.calculate_cost(result, p_prices, w_shipping_costs, w_free_shipping)
    print("ASP solution")
    print(result)
    print(f"Shippings created: {count}")
    print(f"Total shipping cost: {cost}")
    print(f"Total allocations created: {allocations_count}")

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

    solver = Solver("./encodings/encoding.asp")
    solver1 = Solver("./encodings/encoding1.asp")
    solver2 = Solver("./encodings/encoding2.asp")
    generator = Generator()
    
    asp_array_costs = []
    greedy_array_costs = []

    greedy_array_count_warehouses = []
    asp_array_count_warehouses = []
    asp_array_count_warehouses1 = []

    greedy_array_allocations_count = []
    asp_array_allocations_count = []
    asp_array_allocations_count1 = []
    asp_array_allocations_count2 = []

    greedy_run_times = []
    asp_run_times = []
    asp_run_times1 = []
    asp_run_times2 = []
    mnznc_run_times = []
    mnznc_run_times1 = []
    mnznc_run_times2 = []

    greedy_run_times_failed = []
    asp_run_times_failed = []
    asp_run_times_failed1 = []
    asp_run_times_failed2 = []
    mnznc_run_times_failed = []
    mnznc_run_times_failed1 = []
    mnznc_run_times_failed2 = []

    parameters: dict = {}

    created_warehouses = {
        "success": [],
        "failed": []
    }
    created_products = {
        "success": [],
        "failed": []
    }
    iteration_requests = {
        "success": [],
        "failed": []
    }
    
    for _ in tqdm(range(max_runs), desc="Testing..."):
        t_warehouses = random.randint(1, max_warehouses)
        t_products = random.randint(1, max_products)
        ws = enum.Enum("warehouses", [f"w{i+1}" for i in range(t_warehouses)])
        ps = enum.Enum("products", [f"p{i+1}" for i in range(t_products)])
        facts, p_prices, p_requests, w_shipping_costs, w_free_shipping, s_matrix = generator.generate_random_input(t_warehouses, t_products)
        p_requirements = [(i+1, r) for i, r in enumerate(p_requests)]
        greedy = Greedy(t_warehouses, p_requirements, p_prices, w_shipping_costs, w_free_shipping, s_matrix)
        
        # # Greedy
        greedy_result= []
        try:
            start_time_greedy = time.time()
            greedy_result = greedy.allocate_items()
            greedy_execution_time = round(time.time() - start_time_greedy, 2)
            greedy_run_times.append(greedy_execution_time)

            greedy_cost, greedy_count, greedy_allocations_count = greedy.calculate_costs(greedy_result)
            greedy_array_costs.append(greedy_cost)
            greedy_array_count_warehouses.append(greedy_count)
            greedy_array_allocations_count.append(greedy_allocations_count)

            created_warehouses["success"].append(t_warehouses)
            created_products["success"].append(t_products)
            iteration_requests["success"].append(sum(x != 0 for x in p_requests))

        except Exception:
            greedy_execution_time = round(time.time() - start_time_greedy, 2)
            greedy_run_times_failed.append(greedy_execution_time)

            created_warehouses["failed"].append(t_warehouses)
            created_products["failed"].append(t_products)
            iteration_requests["failed"].append(sum(x != 0 for x in p_requests))
        
        # ASP
        asp_result = []
        try:
            start_time_asp = time.time()
            asp_result, interrupted, satisfiable = solver.solve(facts, timeout=timeout)
            asp_execution_time = round(time.time() - start_time_asp, 2)
            if(interrupted and len(greedy_result) > 0):
                asp_run_times.append(timeout)
            elif(interrupted and len(greedy_result) == 0):
                asp_run_times_failed.append(timeout)
            elif(satisfiable):
                asp_run_times.append(asp_execution_time)
            else:
                asp_run_times_failed.append(asp_execution_time)

            asp_cost, asp_count, asp_allocations_count = solver.calculate_cost(asp_result, p_prices, w_shipping_costs, w_free_shipping)
            asp_array_costs.append(asp_cost)
            asp_array_count_warehouses.append(asp_count)
            asp_array_allocations_count.append(asp_allocations_count)

        except Exception as e:
            print(e)

        # ASP1
        asp_result1 = []
        try:
            start_time_asp1 = time.time()
            asp_result1, interrupted, satisfiable = solver1.solve(facts, timeout=timeout)
            asp_execution_time1 = round(time.time() - start_time_asp1, 2)
            if(interrupted and len(greedy_result) > 0):
                asp_run_times1.append(timeout)
            elif(interrupted and len(greedy_result) == 0):
                asp_run_times_failed1.append(timeout)
            elif(satisfiable):
                asp_run_times1.append(asp_execution_time1)
            else:
                asp_run_times_failed1.append(asp_execution_time1)

            _, asp_count1, asp_allocations_count1 = solver1.calculate_cost(asp_result1, p_prices, w_shipping_costs, w_free_shipping)
            asp_array_count_warehouses1.append(asp_count1)
            asp_array_allocations_count1.append(asp_allocations_count1)

        except Exception:
            print(e)

        #ASP2
        asp_result2 = []
        try:            
            start_time_asp2 = time.time()
            asp_result2, interrupted, satisfiable = solver2.solve(facts, timeout=timeout)
            asp_execution_time2 = round(time.time() - start_time_asp2, 2)
            if(interrupted and len(greedy_result) > 0):
                asp_run_times2.append(timeout)
            elif(interrupted and len(greedy_result) == 0):
                asp_run_times_failed2.append(timeout)
            elif(satisfiable):
                asp_run_times2.append(asp_execution_time2)
            else:
                asp_run_times_failed2.append(asp_execution_time2)

            _, _, asp_allocations_count2 = solver2.calculate_cost(asp_result2, p_prices, w_shipping_costs, w_free_shipping)
            asp_array_allocations_count2.append(asp_allocations_count2)

        except Exception as e:
            print(e)
            
        
        # Minizinc
        try:
            parameters["products"] = ps
            parameters["warehouses"] = ws
            parameters["product_in_warehouse"] = s_matrix
            parameters["product_request"] = p_requests
            parameters["product_price"] = p_prices
            parameters["shipping_free_threshold"] = w_free_shipping
            parameters["shipping_fee"] = w_shipping_costs
            mnznc = MinizincSolver("./encodings/marketplace-1.mzn", solver="com.google.ortools.sat")
            start_time_mnznc = time.time()
            result = mnznc.solve(parameters)
            mnznc_execution_time = round(time.time() - start_time_mnznc, 2)
            if(result.solution is not None):
                mnznc_run_times.append(mnznc_execution_time)
            else:
                mnznc_run_times_failed.append(mnznc_execution_time)
            
        except Exception:
            mnznc_execution_time = round(time.time() - start_time_mnznc, 2)
            mnznc_run_times_failed.append(mnznc_execution_time)

        # Minizinc1
        try:
            parameters["shipment_cost"] = asp_cost
            mnznc = MinizincSolver("./encodings/marketplace-2.mzn", solver="com.google.ortools.sat")
            start_time_mnznc = time.time()
            result = mnznc.solve(parameters)
            mnznc_execution_time = round(time.time() - start_time_mnznc, 2)
            if(result.solution is not None):
                mnznc_run_times1.append(mnznc_execution_time + mnznc_run_times[-1])
            else:
                mnznc_run_times_failed1.append(mnznc_run_times_failed[-1])

        except Exception:
            # mnznc_execution_time = round(time.time() - start_time_mnznc, 2)
            mnznc_run_times_failed1.append(mnznc_run_times_failed1[-1])

        # Minizinc2
        try:
            parameters["used_warehouses"] = asp_count
            mnznc = MinizincSolver("./encodings/marketplace-3.mzn", solver="com.google.ortools.sat")
            start_time_mnznc = time.time()
            result = mnznc.solve(parameters)
            mnznc_execution_time = round(time.time() - start_time_mnznc, 2)
            if(result.solution is not None):
                mnznc_run_times2.append(mnznc_execution_time + mnznc_run_times1[-1])
            else:
                mnznc_run_times_failed2.append(mnznc_run_times_failed[-1])

        except Exception:
            # mnznc_execution_time = round(time.time() - start_time_mnznc, 2)
            mnznc_run_times_failed2.append(mnznc_run_times_failed2[-1])

    if len(greedy_run_times) > 0:
        print(f"Solutions found: {len(asp_run_times)}")
        print(f"Success: Greedy-{len(greedy_run_times)} ASP-{len(asp_run_times)} ASP1-{len(asp_run_times1)} ASP2-{len(asp_run_times2)} Minizinc-{len(mnznc_run_times)} Minizinc1-{len(mnznc_run_times1)} Minizinc2-{len(mnznc_run_times2)}")
        print(f"Failed: Greedy-{len(greedy_run_times_failed)} ASP-{len(asp_run_times_failed)} ASP1-{len(asp_run_times_failed1)} ASP2-{len(asp_run_times_failed2)} Minizinc-{len(mnznc_run_times_failed)} Minizinc1-{len(mnznc_run_times_failed1)} Minizinc2-{len(mnznc_run_times_failed2)}")
        print()
        print(f"Mean ASP execution time: {round(mean(asp_run_times),2)}")
        print(f"Mean ASP1 execution time: {round(mean(asp_run_times1),2)}")
        print(f"Mean ASP2 execution time: {round(mean(asp_run_times2),2)}")
        print(f"Total ASP Shippings created: {sum(asp_array_count_warehouses1)}")
        print(f"Total ASP cost: {sum(asp_array_costs)}")
        print(f"Total ASP allocations: {sum(asp_array_allocations_count2)}")
        print()
        print(f"Mean Greedy execution time: {round(mean(greedy_run_times),2)}")
        print(f"Total Greedy Shippings created: {sum(greedy_array_count_warehouses)}")
        print(f"Total Greedy cost: {sum(greedy_array_costs)}")
        print(f"Total Greedy allocations: {sum(greedy_array_allocations_count)}")
        print()
        print(f"Mean Minizinc execution time: {round(mean(mnznc_run_times),2)}")
        print(f"Mean Minizinc1 execution time: {round(mean(mnznc_run_times1),2)}")
        print(f"Mean Minizinc2 execution time: {round(mean(mnznc_run_times2),2)}")

        
        ######## performance ###########
        with open('./statistics/stats-performance@3@2@1-mnznc.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["greedy asp asp1 asp2 mnznc mnznc1 mnznc2"])
            gr = greedy_run_times + greedy_run_times_failed
            asp = asp_run_times + asp_run_times_failed
            asp1 = asp_run_times1 + asp_run_times_failed1
            asp2 = asp_run_times2 + asp_run_times_failed2
            mnznc_ = mnznc_run_times + mnznc_run_times_failed
            mnznc_1 = mnznc_run_times1 + mnznc_run_times_failed1
            mnznc_2 = mnznc_run_times2 + mnznc_run_times_failed2
            for x, y, z, t, w, m, n in zip(gr, asp, asp1, asp2, mnznc_, mnznc_1, mnznc_2):
                writer.writerow([f"{x} {y} {z} {t} {w} {m} {n}"])
                
        ########## cost ############
        with open('./statistics/stats-cost@3.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["greedy asp"])
            for x, y in zip(greedy_array_costs, asp_array_costs):
                writer.writerow([f"{x} {y}"])

        # ####### shippings ###########
        with open('./statistics/stats-shippings@3@2.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["greedy asp asp1"])
            for x, y, z in zip(greedy_array_count_warehouses, asp_array_count_warehouses, asp_array_count_warehouses1):
                writer.writerow([f"{x} {y} {z}"])

        # ####### splits ###########
        with open('./statistics/stats-splits@3@2@1.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["greedy asp asp1 asp2"])
            for x, y, z, t in zip(greedy_array_allocations_count, asp_array_allocations_count, asp_array_allocations_count1, asp_array_allocations_count2):
                writer.writerow([f"{x} {y} {z} {t}"])


    else:
        print("No solutions found")
        
    try:
        with open('./statistics/stats-instances.csv', 'w', newline='') as file:
            ws = created_warehouses["success"] + created_warehouses["failed"]
            ps = created_products["success"] + created_products["failed"]
            itr = iteration_requests["success"] + iteration_requests["failed"]
            writer = csv.writer(file)
            writer.writerow(["t_warehouses t_products p_requests"])
            for x, y, z in zip(ws, ps, itr):
                writer.writerow([f"{x} {y} {z}"])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()