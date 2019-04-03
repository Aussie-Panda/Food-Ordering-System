from ordering_system import OrderingSystem
from mains import Mains
from mains import Mains
from order import Order
# from stock import Stock
from errors import StockError, QuantityError
import pytest

@pytest.fixture
def sys():
	sys = OrderingSystem()
	f1 = Mains('chicken', 5)
	f2 = Mains('duck', 3)
	f3 = Mains('beef', 8)
	f4 = Mains('pen1', 1)
	f5 = Mains('pen2', 2)
	f6 = Mains('pen3', 3)

	# test menu
	sys._menu = [f1, f2, f3, f4, f5, f6]

	return sys


def test_system_and_order(sys):
	
	sys.displayMenu()

	# start ordering

	fl1 = {sys.getFood('chicken'): 3, sys.getFood('duck'): 4, sys.getFood('beef'): 8}
	fl2 = {sys.getFood('pen1'): 4, sys.getFood('pen2'): 8, sys.getFood('pen3'): 9}

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
		

	