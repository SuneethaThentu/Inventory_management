#!/depot/python-2.6.6/bin/python

import os
from random import randint
import json
from Queue import Queue
import traceback

import order
from products import g_products
import inventory

global g_queue

def gen_order_from_file():
    #reading input from input.dat and generating order 
    input_file = os.path.join( os.path.dirname(__file__),"input.dat")
    with open(input_file,"r") as f:
        for ln in f:
            o = json.loads(ln)
            stream = o["stream"]
            header = o["header"]
            del o["stream"]
            del o["header"]
            yield order.Order(stream,header,o)

def init():
    global g_queue
    g_queue = Queue()

if __name__ == '__main__':
    init()
    #intializing the inventory according to statement in project
    inv = inventory.Inventory({"A":150,"B":150,"C":100,"D":100,"E":200})
 
    try:
        orders = gen_order_from_file()
        o = orders.next()
        while True:
            #inserting input order, accepted order, rejecting order values intoglobal queue
            (ordered,allocated,backorderes) = inv.handle_order(o)
            g_queue.put((ordered,allocated,backorderes))

            if not inv.is_empty():
                o = orders.next()
            else:
                print "Inventory Finished. Exiting..."
                #if inventory is empty, printing the order history to standard out.
                #first column  in output indicates customer order (input given by customer)
                #second column in output ideicates the accepted order
                #third column in output indicates the backorders
                while not g_queue.empty():
                    (ordered,allocated,backorderes) = g_queue.get()
                    print "{0} # {1} # {2}".format(ordered,allocated,backorderes)
                #print inv
                break

    except StopIteration:
        # print if no-more orders. still there is some inventory left
        while not g_queue.empty():
            (ordered,allocated,backorderes) = g_queue.get()
            print "{0} # {1} # {2}".format(ordered,allocated,backorderes)

    except:
        traceback.print_exc()

