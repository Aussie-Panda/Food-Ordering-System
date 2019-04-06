from ordering_system import OrderingSystem
from food import Food
from order import Order
from stock import Stock
from errors import StockError, QuantityError, checkStock
from mains import Mains, Burger, Wrap
from drinks import Drinks
from sides import Sides

import pytest

@pytest.fixture
def sys():
	sys = OrderingSystem()
	sys.initMenu()
	# initialise stock
	for category in [sys.stock.mains, sys.stock.drinks, sys.stock.sides, sys.stock.ingredients]:
		for item in category:
			if  item ==  'Fries':
				category[item]  = 100
			elif 'Juice' in item:
				category[item] = 1000
			else:
				category[item] = 10
	# print(sys.stock)
	# sys.displayMenu()
	return sys

def test_getSides(sys):
	testSides = sys.getFood('Fries','med')
	assert (testSides != None)
	assert(testSides.name == 'Fries')
	assert(testSides.size == 'med')
	assert(testSides.volumn == 40)
	assert(testSides.price ==  2)

	s2 = sys.getFood('ddd', 'sml')
	assert (s2 == None)

def test_getMains(sys):
	testMains = sys.getFood('Burger')
	assert(testMains.name == 'Burger')
	assert(testMains.price == 5)

	m2 = sys.getFood('fff')
	assert (m2 == None)

def test_getDrinks(sys):
	testDrinks = sys.getFood('Lemonade', 'Cans')
	assert(testDrinks.name == 'Lemonade')
	assert(testDrinks.price == 3)
	assert(testDrinks.volumn == 375)

	d2 = sys.getFood('Lemonade', 'sml')
	assert(d2 == None)

	d3 = sys.getFood('Orange_Juice', 'sml')
	assert(d3.volumn == 250)

	d4 = sys.getFood('Apple_Juice')
	assert(d4 == None)
	
def test_make_order(sys):
	orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	order, errors = sys.makeOrder(orderedFood)
	assert(not errors)
	assert(order.computeNetPrice() == 12)
	assert(sys.stock.sides['Nuggets'] == 1)
	assert(sys.stock.drinks['Lemonade(Cans)'] == 7 )

def test_make_order_buger(sys):
	burger = sys.getFood('Burger')
	burger.addBuns(3)
	burger.addPats(2)
	burger.changeIngredients('tomato', 2)
	burger.changeIngredients('cheddar_cheese', 3)
	orderedFood = {burger: 1, sys.getFood('Orange_Juice','sml'): 2}
	order, errors = sys.makeOrder(orderedFood)
	# print(sys.stock)
	assert(not errors)
	assert(order.computeNetPrice() == 24)

	assert(sys.stock.drinks['Orange_Juice'] == 500)
	assert(sys.stock.ingredients['tomato'] == 8)
	assert(sys.stock.ingredients['cheddar_cheese'] == 7)
	assert(sys.stock.ingredients['buns'] == 7)
	assert(sys.stock.ingredients['patties'] == 8)
	assert(sys.stock.mains['Burger'] == 9)

def test_make_order_wrap(sys):
	wrap = sys.getFood('Wrap')
	wrap.addPats(3)
	wrap.changeIngredients('tomato_sauce', 3)
	orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
	order, errors = sys.makeOrder(orderedFood)
    
	assert(not errors)
	assert(order.computeNetPrice() == 16)

	assert(sys.stock.sides['Fries'] == 40)
	assert(sys.stock.mains['Wrap'] == 9)
	assert(sys.stock.ingredients['tomato_sauce'] == 7)

def test_out_of_stock(sys):
	orderedFood = {sys.getFood('Nuggets', 'lrg'): 10, sys.getFood('Fries','sml'): 1}
	order, errors = sys.makeOrder(orderedFood)
	assert(len(errors) == 1 and 'Nuggets' in errors)
	assert(order == None)

	orderedFood = {sys.getFood('Orange_Juice', 'med'): 3, sys.getFood('Fries','sml'): 1}
	order, errors = sys.makeOrder(orderedFood)
	assert(len(errors) == 1 and 'Orange_Juice' in errors)
	assert(order == None)

	orderedFood = {sys.getFood('Lemonade', 'Bottles'): 11, sys.getFood('Fries','sml'): 1}
	order, errors = sys.makeOrder(orderedFood)
	assert(len(errors) == 1 and 'Lemonade(Bottles)' in errors)
	assert(order == None)

def test_modify_order(sys):
	orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Fries','lrg'): 15 , sys.getFood('Fries','sml'): 8}
	order, errors = sys.makeOrder(orderedFood)
	assert(len(errors) == 1 and 'Fries' in errors)
	assert(order == None)

	sys.modifyOrder(orderedFood, sys.getFood('Fries', 'lrg'), 1)
	sys.modifyOrder(orderedFood, sys.getFood('Fries', 'sml'), 1)
	# expected orderedFood: {smlNuggets: 3, lrgFries: 1, smlFries: 1}
	order, errors = sys.makeOrder(orderedFood)
	assert(not errors)
	assert(order.computeNetPrice() == 7)

	print(sys.stock)
	sys.modifyOrder(orderedFood, sys.getFood('Orange_Juice', 'med'), 2)
	sys.modifyOrder(orderedFood, sys.getFood('Nuggets', 'sml'), 0)
	sys.modifyOrder(orderedFood, sys.getFood('Fries', 'lrg'), 0)
	# expected orderedFood: {smlFries: 1, medOrange_Juice: 2}	
	assert(len(orderedFood) == 2)
	order,errors = sys.makeOrder(orderedFood)
	assert(not errors)
	assert(order.computeNetPrice() == 9)

def test_getNextOrder_if_id_not_found(sys):
	orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	order, errors = sys.makeOrder(orderedFood)
	testGet = sys.getNextOrder(None,2)
	assert(testGet == None)

def test_getNextOrder_if_id_found(sys):
	orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	order, errors = sys.makeOrder(orderedFood)
	testGet = sys.getNextOrder(None,1)
	assert(testGet == order)

def test_getNextOrder_if_stat_not_found(sys):
	orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	order, errors = sys.makeOrder(orderedFood)
	testGet = sys.getNextOrder('something')
	assert(testGet == None)

def test_getNextOrder_if_stat_found(sys):
	orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	order, errors = sys.makeOrder(orderedFood)
	testGet = sys.getNextOrder('Pending')
	assert(testGet == order)

def test_getNextOrder_with_multiple_orders(sys):
	orderedFood1 = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	burger = sys.getFood('Burger')
	burger.addBuns(3)
	burger.addPats(2)
	burger.changeIngredients('tomato', 2)
	burger.changeIngredients('cheddar_cheese', 3)
	orderedFood2 = {burger: 1, sys.getFood('Orange_Juice','sml'): 2}
	order, errors = sys.makeOrder(orderedFood1)
	order2, errors = sys.makeOrder(orderedFood2)
	testGet = sys.getNextOrder('Pending')
	assert(testGet == order)
	order.updateOrder('someStat')
	testGet = sys.getNextOrder('someStat')
	assert(testGet == order)
	testGet = sys.getNextOrder('Pending')
	assert(testGet == order2)
	testGet = sys.getNextOrder(None,2)
	assert(testGet == order2)
	testGet = sys.getNextOrder(None,100)
	assert(testGet == None)

def test_deleteOrder_if_id_not_found(sys):
	wrap = sys.getFood('Wrap')
	wrap.addPats(3)
	wrap.changeIngredients('tomato_sauce', 3)
	orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
	order, errors = sys.makeOrder(orderedFood)
	testDelete = sys.deleteOrder(None, 3)
	assert(testDelete == None)
	assert(len(sys.order) == 1)

def test_deleteOrder_if_id_found(sys):
	wrap = sys.getFood('Wrap')
	wrap.addPats(3)
	wrap.changeIngredients('tomato_sauce', 3)
	orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
	order, errors = sys.makeOrder(orderedFood)
	testDelete = sys.deleteOrder(None, 1)
	assert(testDelete == order)
	assert(len(sys.order) == 0)

def test_deleteOrder_if_stat_not_found(sys):
	wrap = sys.getFood('Wrap')
	wrap.addPats(3)
	wrap.changeIngredients('tomato_sauce', 3)
	orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
	order, errors = sys.makeOrder(orderedFood)
	testDelete = sys.deleteOrder('someStat')
	assert(testDelete == None)
	assert(len(sys.order) == 1)

def test_deleteOrder_if_stat_found(sys):
	wrap = sys.getFood('Wrap')
	wrap.addPats(3)
	wrap.changeIngredients('tomato_sauce', 3)
	orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
	order, errors = sys.makeOrder(orderedFood)
	testDelete = sys.deleteOrder('Pending')
	assert(testDelete == order)
	assert(len(sys.order) == 0)

def test_delete_multiple_orders(sys):
	orderedFood1 = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	burger = sys.getFood('Burger')
	burger.addBuns(3)
	burger.addPats(2)
	burger.changeIngredients('tomato', 2)
	burger.changeIngredients('cheddar_cheese', 3)
	orderedFood2 = {burger: 1, sys.getFood('Orange_Juice','sml'): 2}
	order, errors = sys.makeOrder(orderedFood1)
	order2, errors = sys.makeOrder(orderedFood2)
	testDelete = sys.deleteOrder('something')
	assert(testDelete == None)
	assert(len(sys.order) == 2)
	order.updateOrder('someStat')
	testDelete = sys.deleteOrder('someStat')
	assert(testDelete == order)
	assert(len(sys.order) == 1)
	testDelete = sys.deleteOrder(None,2)
	assert(testDelete == order2)
	assert(len(sys.order) == 0)

# def test_modify_order_with_exception(sys):
# 	orderedFood = {sys.getFood('Nuggets','sml'): 3}
# 	sys.stock.addQuantity('Nuggets', 0)
# 	newOrder, errors = sys.modifyOrder(orderedFood, orderedFood.keys(), 1)
# 	assert(len(errors) != 0)
	
# def test_system_and_order(sys):
# 	pass
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

	