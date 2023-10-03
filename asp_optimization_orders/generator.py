import random

max_shipping_cost = 20
max_price = 10
max_request_allowed = 20
max_stock = 30
max_free_shipping_threshold = 60

class Generator:

    def __init__(self):
        self.__product_prices = []
        self.__shippings_costs = []
        self.__shipping_thresholds = []

    def get_product_prices(self):
        return self.__product_prices

    def get_shippings_costs(self):
        return self.__shippings_costs
    
    def get_shippings_thresholds(self):
        return self.__shipping_thresholds

    def generate_random_input(self, t_warehouse, t_products, set_seed=False, seed=123432):
        
        if set_seed:
            random.seed(seed)
        output = "products({}).".format(t_products)
        facts = []
        
        products_prices = []
        products_requests = []
        warehouses_shipping_costs = []
        warehouses_free_shipping = []
        stocks_matrix = [[0 for _ in range(t_warehouse)]]*t_products
        
        # warehouse and product facts
        for p in range(1, t_products+1):
            facts.append("product({}).".format(p))
            price = random.randint(1, max_price)
            request = random.randint(0, max_request_allowed)
            self.__product_prices.append(price)
            facts.append("product_price({}, {}).".format(p, price))
            facts.append("product_request({}, {}).".format(p, request))
            products_prices.append(price)
            products_requests.append(request)
        
        for w in range(1, t_warehouse+1):
            facts.append("warehouse({}).".format(w))
            shipping_cost = random.randint(1, max_shipping_cost)
            free_shipping_threshold = random.randint(1, max_free_shipping_threshold)
            self.__shippings_costs.append(shipping_cost)
            self.__shipping_thresholds.append(free_shipping_threshold)
            facts.append("warehouse_shipping_cost({}, {}).".format(w, shipping_cost))
            facts.append("warehouse_free_shipping({}, {}).".format(w, free_shipping_threshold))
            warehouses_shipping_costs.append(shipping_cost)
            warehouses_free_shipping.append(free_shipping_threshold)

        # stocks facts
        for p in range(1, t_products+1):
            p_stocks = []
            for w in range(1, t_warehouse+1):
                stock = random.randint(0, max_stock)
                facts.append("products_in_warehouse({}, {}, {}).".format(p, w, stock))
                p_stocks.append(stock)
            stocks_matrix[p-1] = p_stocks

        facts = " ".join(facts)


        output = f"{output} {facts}"
        
        return output, products_prices, products_requests, warehouses_shipping_costs, warehouses_free_shipping, stocks_matrix

    def calculate_cost(self, allocations: list[dict]):
        warehouses = set()
        for al in allocations:
            warehouse_key = list(al.keys())[1]
            warehouses.add(al[warehouse_key])
        return sum(self.__shippings_costs[w-1] for w in warehouses)