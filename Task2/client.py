from ordering_system import OrderingSystem
from stock import Stock

from sides import Sides

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

print("\n\n~~~~~Print Menu~~~~~")
system.displayMenu()

print("\n\n~~~~~Print Stock~~~~~")
print(system.stock)

# food list example
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