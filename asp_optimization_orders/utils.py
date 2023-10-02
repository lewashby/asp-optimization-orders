

def read_file(dir):
    file = open(dir, "r")
    data = file.read()
    file.close()
    return data

def create_json_object(result):
    splitted = result.split(',')
    return {
        "product": int(splitted[0][-1]), 
        "warehouse": int(splitted[1][0]), 
        "quantity": int(splitted[2][0])
    }

def parse_response(result):
    res = filter(lambda x: x["quantity"] != 0, map(lambda y: create_json_object(y), result))
    return list(res)

def logger(code, msg):
    return