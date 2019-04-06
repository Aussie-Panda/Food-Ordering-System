from ordering_system import OrderingSystem
from order import Order
from stock import Stock

system = OrderingSystem()
system.initMenu()
# initialise stock
for category in [system.stock.mains, system.stock.drinks, system.stock.sides, system.stock.ingredients]:
	for item in category:
		if  item ==  'Fries':
			category[item]  = 1000
		elif 'Juice' in item:
			category[item] = 1000
		else:
			category[item] = 10

print("~~~~~Print Menu~~~~~")
system.displayMenu()

print("\n\n~~~~~Print Stock~~~~~")
print(system.stock)

# customer order food
fl1 =  {system.getFood('Nuggets','sml'): 3, system.getFood('Fries','lrg'): 4, system.getFood('Fries','sml'): 8}
fl2 = {system.getFood('Fries','med'): 4, system.getFood('Fries', 'sml'): 8, system.getFood('Lemonade','Cans'): 9}

print("\n\n~~~~~~~~Make First Order~~~~~~~~")
o1,errors = system.makeOrder(fl1)
assert(not errors)
receipt = system.printReceipt(o1)
print(receipt)

print("\n\n~~~~~~~~Make Second Order~~~~~~~~")
o2, errors = system.makeOrder(fl2)
assert(not errors)
receipt = system.printReceipt(o2)
print(receipt)

print("\n\n~~~~~~~~Print All Orders~~~~~~~~")
for o in system.order:
	print(o)
	print('\n')

# staff serving order
while (len(system.order) > 0):
	curr_order = system.getNextOrder('Pending')
	print(f"\n\n~~~~~~~~~~Now Serving Order {curr_order.orderId}~~~~~~~~")

	curr_order.updateOrder('Preparing')
	print(curr_order)
	print("\n~~~~~~~~Order is Ready~~~~~~~~")
	curr_order.updateOrder('Ready')
	print(curr_order)
	print("\n~~~~~~~~Order Picked Up~~~~~~~")
	curr_order.updateOrder('Picked Up')
	system.deleteOrder(None, curr_order.orderId)
	print(f"Order {curr_order.orderId} has been picked up.")
	
