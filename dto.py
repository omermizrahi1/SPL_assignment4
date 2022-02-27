# Data Transfer Objects:
class Hat:
    def __init__(self, id, topping, supplier, quantity):
        self.id = id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity

    def __init__(self, hat_lists):
        self.id = hat_lists[0]
        self.topping = hat_lists[1]
        self.supplier = hat_lists[2]
        self.quantity = hat_lists[3]

    def __str__(self):
        return [self.id, self.supplier, self.supplier, self.quantity]


class Supplier:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __init__(self, suppliers_list):
        self.id = suppliers_list[0]
        self.name = suppliers_list[1]


class Order:
    def __init__(self, id, location, hat):
        self.id = id
        self.location = location
        self.hat = hat
