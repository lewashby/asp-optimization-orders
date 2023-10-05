from functools import reduce

class Greedy:

    def __init__(self, t_warehouses, products_requirements, p_prices, w_shipping_costs, w_shipping_threshold, s_matrix):
        self.__t_warehouses = t_warehouses
        self.__stocks_matrix = s_matrix
        self.__products_requirements = list(filter(lambda x: x[1] != 0, products_requirements))
        self.__products_prices = p_prices
        self.__w_shipping_costs = w_shipping_costs
        self.__w_shipping_threshold = w_shipping_threshold

    
    def get_stock_value(self, p, w):
        return self.__stocks_matrix[p-1][w-1]


    def allocate_items(self):

        available_warehouses = [i for i in range(1, self.__t_warehouses+1)]
        requirements = self.__products_requirements

        def iteration(available_warehouses, requirements):

            if (len(requirements) == 0): return dict()

            elif (len(requirements) > 0 and len(available_warehouses) == 0): raise RuntimeError("No solution")

            updated_requirements = []
            updated_available_warehouses = []
            allocations = dict()

            best_warehouse = self.get_most_weighted_warehouse(available_warehouses, requirements)
            for product_id, product_quantity in requirements:
                p_stock = self.get_stock_value(product_id, best_warehouse)
                if (p_stock > 0):
                    quantity = min(p_stock, product_quantity)
                    if (product_quantity > p_stock):
                        updated_requirements.append((product_id, product_quantity-quantity))

                    if (best_warehouse in allocations):
                        allocations[best_warehouse].append((product_id, quantity))
                    else:
                        allocations[best_warehouse] = [(product_id, quantity)]
                else:
                    updated_requirements.append((product_id, product_quantity))

            updated_available_warehouses = list(set(available_warehouses) - set(allocations.keys()))

            return allocations | iteration(updated_available_warehouses, updated_requirements)
        
        return iteration(available_warehouses, requirements)


    # requirements list<pair(product_id, quantity)>
    def get_most_weighted_warehouse(self, available_warehouses: list, requirements: list):

        warehouses_weights = dict()
        for w in available_warehouses:
            for product_id, product_quantity in requirements:
                product_stock_in_warehouse = self.get_stock_value(product_id, w)
                quantity = min(product_quantity, product_stock_in_warehouse)
                if product_stock_in_warehouse > 0:
                    if w in warehouses_weights:
                        warehouses_weights[w] += quantity
                    else:
                        warehouses_weights[w] = quantity
        
        warehouses_weights = sorted(warehouses_weights, reverse=True)
        
        return next(iter(warehouses_weights))
    
    def calculate_costs(self, allocations: dict):
        total = 0
        for w in allocations.keys():
            index = w-1
            cost = self.__w_shipping_costs[index]
            products = allocations[w]
            spent = reduce(lambda result, y: result + y[1]*self.__products_prices[y[0]-1], products, 0)
            if spent >= self.__w_shipping_threshold[index]:
                cost = 0
            total+=cost
        allocations_count = reduce(lambda result, y: result + len(allocations[y]), allocations.keys(), 0)
        return total, len(allocations.keys()), allocations_count


