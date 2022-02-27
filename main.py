import sys
from dto import Hat, Supplier, Order
from repository import repo

# returns a tuple of hat lists and suppliers lists
def parse_config_file(path):
    lines, hats, suppliers = [], [], []
    with open(path) as config_file:
        for line in config_file:
            lines.append(cut_order_line(line))
        nums = lines.pop(0).split(',')
        num_of_hats = int(nums[0])
        num_of_suppliers = int(nums[1])
        for line in lines[:num_of_hats]:
            hats.append(parse_partial_ints_list(line.split(',')))
        for line in lines[num_of_hats:num_of_suppliers + num_of_hats]:
            suppliers.append(parse_partial_ints_list(line.split(',')))
        return hats, suppliers


def parse_partial_ints_list(_list):
    new_list = []
    for a in _list:
        try:
            new_list.append(int(a))
        except ValueError:
            new_list.append(a)
    return new_list


def cut_order_line(line):
    if line[-1] == '\n':
        return line[:-1]
    return line


def parse_orders(path):
    lines, orders, index = [], [], 1
    with open(path) as orders_file:
        for line in orders_file:
            orders.append([index] + cut_order_line(line).split(','))
            index += 1
    return orders


def insert_into_tables(hats, suppliers):
    for hat in hats:
        repo.hats.insert(hat)
    for supplier in suppliers:
        repo.suppliers.insert(supplier)


def list_to_object(objects_list, class_type):
    objects = []
    for o in objects_list:
        objects.append(class_type(o))
    return objects


def get_all_toppings_rows(topping):
    command = """SELECT * FROM hats WHERE topping like ? ORDER BY supplier ASC;"""
    c = repo._conn.cursor()
    hats_c = c.execute(command, [topping]).fetchall()
    hats = []
    for hat in hats_c:
        hats.append(Hat(hat))
    return hats


def remove_hat_from_stock(hat):
    command = """UPDATE hats SET quantity = ? WHERE id = ?"""
    repo._conn.execute(command,[hat.quantity-1, hat.id])

def choose_hat(hats):
    for hat in hats:
        if hat.quantity!=0:
            return hat
    return None


def order(order_details):
    index, location, topping = order_details
    av_hats = get_all_toppings_rows(topping)
    hat = choose_hat(av_hats)
    if hat != None:
        remove_hat_from_stock(hat)
        new_order = Order(index, location, hat)
        repo.orders.insert(new_order)


def order_all(order_list):
    for order_details in order_list:
        order(order_details)


def get_orders():
    command = """SELECT hats.topping, suppliers.name, orders.location
                 FROM orders  
                 LEFT JOIN hats
                 ON hats.id = orders.hat
                 LEFT JOIN  suppliers
                 ON suppliers.id = hats.supplier """
    c = repo._conn.cursor()
    orders_c = c.execute(command).fetchall()
    orders = [list(i) for i in orders_c]
    return orders


def create_output_file(orders, output_file_name):
    output = ''
    for _order in orders:
        output += order_to_string(_order) + '\n'
    f = open(output_file_name, "w+")
    f.write(output[:-1])
    f.close()


def order_to_string(li):
    order_str = li[0] + ',' + li[1] + ',' + li[2]
    return order_str


def delete_hats_with_zero_quantity():
    command = """DELETE FROM hats WHERE quantity = 0;"""
    repo._conn.execute(command)


if __name__ == '__main__':
    config_file_name, orders_file_name, output_file_name = sys.argv[1], sys.argv[2], sys.argv[3]
    hats_list, suppliers_lists = parse_config_file(config_file_name)
    orders_list = parse_orders(orders_file_name)
    hats, suppliers = list_to_object(hats_list, Hat), list_to_object(suppliers_lists, Supplier)
    repo.create_tables()
    insert_into_tables(hats, suppliers)
    order_all(orders_list)
    orders = get_orders()
    create_output_file(orders, output_file_name)
    delete_hats_with_zero_quantity()

