#!/depot/python-2.6.6/bin/python

from products import g_products

class InvalidOrderError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class Order:
    def __init__(self,stream,header,kv_hash):
        allowed_products = g_products
        #self.__dict__.update((k,v) for k,v in kv_hash.iteritems() if k in allowed_products)

        self.A = kv_hash.get("A",0)
        self.B = kv_hash.get("B",0)
        self.C = kv_hash.get("C",0)
        self.D = kv_hash.get("D",0)
        self.E = kv_hash.get("E",0)

        self.stream = stream
        self.header = header

        values = [v for k,v in kv_hash.iteritems() if hasattr(self,k)]
        valid_values = [ True if (v >= 0 and v<= 5) else False for v in values ]

        if not all(valid_values):
            raise InvalidOrderError("Invalid Order. Some values  are not in the range 0..5")

        if all([ True if ( v < 1 or v > 6) else False for v in values ]):
            raise InvalidOrderError("Invalid Order. Atleast one line item should  be in the range 1..5")

    def __str__(self):
        return repr(self.__dict__)

    def as_dict(self):
        return self.__dict__

    def get_demand(self,product):
        return getattr(self,product)

