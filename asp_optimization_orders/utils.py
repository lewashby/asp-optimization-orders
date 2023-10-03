from functools import reduce

def read_file(dir):
    file = open(dir, "r")
    data = file.read()
    file.close()
    return data

def create_json_object(result):
    values = result[result.find("(")+1:result.find(")")]
    splitted = values.split(',')
    return {
        "warehouse": int(splitted[1]), 
        "product": int(splitted[0]), 
        "quantity": int(splitted[2])
    }

def parse_response(result):
    res = filter(lambda x: x["quantity"] != 0, map(lambda y: create_json_object(y), result))
    return list(res)

def logger(code, msg):
    return

def calculate_cost(result: list, p_prices: list, w_shipping_cost: list, w_threshold: list):
    total = 0

    for i, cost in enumerate(w_shipping_cost):
        index = i+1
        warehouse_allocations = list(filter(lambda x: x['warehouse'] == index, result))
        if (len(warehouse_allocations) > 0):
            spent = reduce(lambda sum, x: sum + x['quantity']*p_prices[x['product']-1], warehouse_allocations, 0)
            if spent > w_threshold[i]:
                cost = 0
            total+=cost
    return total
