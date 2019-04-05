from ordering_system import OrderingSystem
from mains import Mains
from mains import Mains
from order import Order
from stock import Stock
from errors import StockError, QuantityError
import pytest

@pytest.fixture
def sys():
	sys = OrderingSystem()
	sys.initMenu()
	return sys

def test_getSides(sys):
	testSides = sys.getFood('Fries','med')
	assert(testSides.name == 'Fries')
	assert(testSides.size == 'med')

# def test_getMains(sys):
# 	testMains = sys.getFood('Burger')
# 	assert(testMains.name == 'Burger')
# 	assert(testMains.price == 5)

# def test_getDrinks(sys):
# 	pass

# def test_make_order_with_exception(sys):
# 	orderedFood = {sys.getFood('Nuggets','sml'): 3}
# 	sys.stock.addQuantity('Nuggets', 2)
# 	order, errors = sys.makeOrder(orderedFood)
# 	assert(len(errors) != 0)
# 	assert(order == None)

# def test_make_order(sys):
# 	orderedFood = {sys.getFood('Nuggets','sml'): 3}
# 	sys.stock.addQuantity('Nuggets', 100)
# 	order, errors = sys.makeOrder(orderedFood)
# 	assert(order != None)

def test_modify_order_with_exception(sys):
	orderedFood = {sys.getFood('Nuggets','sml'): 3}
	sys.stock.addQuantity('Nuggets', 0)
	newOrder, errors = sys.modifyOrder(orderedFood, orderedFood.keys(), 1)
	assert(len(errors) != 0)
	
def test_system_and_order(sys):
	pass
	#def getFood(self,name,size=None):
	# start ordering
	#fl1 and fl2 are both dic 
	# fl1 = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Fries','lrg'): 4, sys.getFood('Fries','sml'): 8}
	# fl2 = {sys.getFood('Fries','med'): 4, sys.getFood('Fries', 'sml'): 8, sys.getFood('Lemonade(Can)'): 9}

	# testSides2 = sys.getFood('Fries','sml'): 10,sys.getFood('Fries','lrg'): 3,sys.getFood('Nuggets','sml'): 4,sys.getFood('Nuggets','lrg'): 4}
	'''
	# test makeOrder() and computeNetPrice()
	o1, errors = sys.makeOrder(fl1)
	assert(not errors)
	price = o1.computeNetPrice()
	assert(price == 91)
	sys.sendReceipt(o1)
	o2, errors = sys.makeOrder(fl2)
	assert(not errors)
	price = o2.computeNetPrice()
	assert(price == 47)
	sys.sendReceipt(o2)
	
	
	# test getNextOrder()
	nextOrder = sys.getNextOrder("Pending")
	assert(nextOrder.orderId == 1)
	nextOrder = sys.getNextOrder(None,2)
	assert(nextOrder.orderId == 2)
	nextOrder = sys.getNextOrder(None, 3)
	assert(not nextOrder)
	nextOrder = sys.getNextOrder("random")
	assert(not nextOrder)

	# test modifyOrder()
	f7 = Mains('eraser', 3)
	o2.modifyOrder(f7,3)
	assert(len(o2.orderedItem) == 4)
	
	o2.modifyOrder(f7,0)
	assert(len(o2.orderedItem) == 3)
	assert(f7 not in o2.orderedItem)

	o2.modifyOrder(sys.getFood('pen1'), 2)
	assert(o2.orderedItem[o2.getFood('pen1')] == 2)

	# test updateOrder() and deleteOrder()	
	o2.updateOrder("Ready")
	trashOrder = sys.deleteOrder("Ready")
	trashOrder = sys.deleteOrder(None,1)
	assert(not sys.order)
	'''

	