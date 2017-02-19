#!/depot/python-2.6.6/bin/python

from products import g_products
import threading

import logging

class NoSuchProduct(Exception):
    def __init__(self,product):
        self.msg = "No Such Product Exists: %s" % (product,)

    def __str__(self):
        return repr(self.msg)

class InsufficientStock(Exception):
    def __init__(self,product,current_stock,demand):
        self.product = product
        self.current_stock = current_stock
        self.demand = demand
        self.msg = "Insufficient Stock of product %s. Current Stock: %r. Demand: %r" % (product,current_stock,demand)

    def __str__(self):
        return repr(self.msg)

    def get_product(self):
        return self.product

    def get_current_stock(self):
        return self.current_stock

    def get_demand(self):
        return self.demand

class Inventory:
    def __init__(self,kv_hash):

        allowed_products = g_products
        self.__dict__.update((k,v) for k,v in kv_hash.iteritems() if k in allowed_products)
        self.lock = threading.Lock()

    def consume_product(self,product,demand):

        if not hasattr(self,product):
            raise NoSuchProduct(product)
        else:
            current_stock = eval("self.%s" % (product,))
            if current_stock < demand:
                raise InsufficientStock(product,current_stock,demand)
            else:
                exec("self.%s = self.%s - demand" % (product,product))

    def __str__(self):
        #values = { p:getattr(self,p) for p in g_products}
        values={}
        for p in g_products:
            values.update({p:getattr(self,p)})
        return repr(values)

    def is_empty(self):
        values = [getattr(self,p) for p in g_products]
        if all([v == 0 for v in values]):
            print "Inventory is emty..."
            return True
        else:
            return False

    def handle_order(self,order):
        # will raise insufficient stock and invalid orders and halt if the orders are
        #invalid or if the order is valid return the input,accepted order,backorderd
        with self.lock:
            back_order = {}
            catered_order = {}
            for p in g_products:
                try:
                    self.consume_product(p,order.get_demand(p))
                except NoSuchProduct:
                    logging.warn("Invalid Product {0} in the order {1}".format(p,order))

                    pass
                except InsufficientStock,e:
                    logging.warn("Insufficient stock of product {0} (available: {1}, requested: {2}) in the order {3}".format(p,e.get_current_stock(),e.get_demand(),order))

                    back_order[p] = e.get_demand()
                    catered_order[p] = 0
                else:
                    back_order[p] = 0
                    catered_order[p] = order.get_demand(p)

            return ((order,catered_order,back_order))
