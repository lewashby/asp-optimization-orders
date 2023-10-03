
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
