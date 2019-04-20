from src.ordering_system import OrderingSystem
from src.food import Food
from src.order import Order
from src.stock import Stock
from src.mains import Mains, Burger, Wrap
from src.drinks import Drinks
from src.sides import Sides
from src.errors import *
from init import bootstrap_system
import pytest

@pytest.fixture
def sys():
	sys = bootstrap_system()
	return sys


def test_getSides_without_error(sys):
	# print(sys.stock)
	testSides = sys.getFood('Fries','med')
	assert (testSides != None)
	assert(testSides.name == 'Fries')
	assert(testSides.size == 'med')
	assert(testSides.volumn == 40)
	assert(testSides.price ==  2)
	print('pass the test: ')

def test_getSides_with_errors(sys):
	s2 = None
	try:
		s2 = sys.getFood('ddd', 'sml')
	except SearchError as er:
		# print('capture error:',er)
		assert(True)
	else:
		assert(False)
	print('pass the test: ')


def test_getMains_without_error(sys):
	testMains = sys.getFood('Burger')
	assert(testMains.name == 'Burger')
	assert(testMains.price == 5)
	print('pass the test: ')

def test_getMains_with_error(sys):
	m2 = None
	try:
		m2 = sys.getFood('fff')
	except SearchError as er:
		assert(True)
	else:
		assert(False)
	assert (m2 == None)
	print('pass the test: ')

def test_getDrinks_without_error(sys):
	testDrinks = sys.getFood('Lemonade', 'Cans')
	assert(testDrinks.name == 'Lemonade')
	assert(testDrinks.price == 3)
	assert(testDrinks.volumn == 375)
	d3 = sys.getFood('Orange_Juice', 'sml')
	assert(d3.volumn == 250)
	print('pass the test: ')

def test_getDrinks_with_error(sys):
	d2 = None

	try:
		d2 = sys.getFood('Lemonade', 'sml')

	except SearchError as er:
		assert(True)
	else:
		assert(False)
	assert(d2 == None)

	print('pass the test: ')

def test_getDrinks_with_error2(sys):

	d4 = None
	try:

		d4 = sys.getFood('Apple_Juice')
	except SearchError as er:
		assert(True)
	else:
		assert(False)

	assert(d4 == None)
	print('pass the test: ')

def test_make_order(sys):
	# orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	order = sys.makeOrder()
	nuggets = sys.getFood('Nuggets','sml')
	lemon = sys.getFood('Lemonade', 'Cans')
	order.addFood(nuggets,3)
	order.addFood(lemon,3)
	sys.confirmOrder(order)
	# assert(not errors)
	assert(order.computeNetPrice() == 12)
	assert(sys.stock.sides['Nuggets'] == 9991)
	assert(sys.stock.drinks['Lemonade(Cans)'] == 9997 )

def test_make_order_buger(sys):
	order = sys.makeOrder()
	burger = sys.getFood('Burger')
	burger.addOn['Buns'] = 3
	burger.addOn['Patties'] = 2
	burger.changeIngredients('tomato', 2)
	burger.changeIngredients('cheddar_cheese', 3)
	order.addFood(burger,1)
	orange = sys.getFood('Orange_Juice','sml')
	order.addFood(orange,2)
	# orderedFood = {burger: 1, sys.getFood('Orange_Juice','sml'): 2}
	# order, errors = sys.makeOrder(orderedFood)
	# print(sys.stock)
	sys.confirmOrder(order)
	# assert(not errors)
	assert(order.computeNetPrice() == 24)

	assert(sys.stock.drinks['Orange_Juice'] == 9500)
	assert(sys.stock.ingredients['tomato'] == 9998)
	assert(sys.stock.ingredients['cheddar_cheese'] == 9997)
	assert(sys.stock.ingredients['buns'] == 9997)
	assert(sys.stock.ingredients['patties'] == 9998)
	assert(sys.stock.mains['Burger'] == 9999)

def test_make_order_wrap(sys):
	order = sys.makeOrder()
	wrap = sys.getFood('Wrap')
	wrap.addOn['Patties'] = 3
	wrap.changeIngredients('tomato_sauce', 3)
	order.addFood(wrap,1)
	fries = sys.getFood('Fries', 'lrg')
	# orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
	# order.addFood(wrap,1)
	order.addFood(fries,1)
	sys.confirmOrder(order)
	# assert(not errors)
	assert(order.computeNetPrice() == 16)

	assert(sys.stock.sides['Fries'] == 9940)
	assert(sys.stock.mains['Wrap'] == 9999)
	assert(sys.stock.ingredients['tomato_sauce'] == 9997)

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

# def test_modify_order(sys):
# 	orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Fries','lrg'): 15 , sys.getFood('Fries','sml'): 8}
# 	order, errors = sys.makeOrder(orderedFood)
# 	assert(len(errors) == 1 and 'Fries' in errors)
# 	assert(order == None)

# 	sys.modifyOrder(orderedFood, sys.getFood('Fries', 'lrg'), 1)
# 	sys.modifyOrder(orderedFood, sys.getFood('Fries', 'sml'), 1)
# 	# expected orderedFood: {smlNuggets: 3, lrgFries: 1, smlFries: 1}
# 	order, errors = sys.makeOrder(orderedFood)
# 	assert(not errors)
# 	assert(order.computeNetPrice() == 7)

# 	print(sys.stock)
# 	sys.modifyOrder(orderedFood, sys.getFood('Orange_Juice', 'med'), 2)
# 	sys.modifyOrder(orderedFood, sys.getFood('Nuggets', 'sml'), 0)
# 	sys.modifyOrder(orderedFood, sys.getFood('Fries', 'lrg'), 0)
# 	# expected orderedFood: {smlFries: 1, medOrange_Juice: 2}	
# 	assert(len(orderedFood) == 2)
# 	order,errors = sys.makeOrder(orderedFood)
# 	assert(not errors)
# 	assert(order.computeNetPrice() == 9)

def test_getNextOrder_if_id_not_found(sys):
	# orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	# order, errors = sys.makeOrder(orderedFood)
	order = sys.makeOrder()
	testGet = None
	try:
		testGet = sys.getNextOrder(None,2)
	except SearchError as er:
		assert(True)
	else: 
		assert(False)
	assert(testGet == None)

def test_getNextOrder_if_id_found(sys):
	# orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	# order, errors = sys.makeOrder(orderedFood)
	order = sys.makeOrder()
	testGet = sys.getNextOrder(None,1)
	assert(testGet == order)

def test_getNextOrder_if_stat_not_found(sys):
	# orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	# order, errors = sys.makeOrder(orderedFood)
	order = sys.makeOrder()
	testGet = None
	
	try:
		testGet = sys.getNextOrder('something',None)
	except SearchError as er:
		assert(True)
	else: 
		assert(False)
	assert(testGet == None)

def test_getNextOrder_if_stat_found(sys):
	# orderedFood = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
	# order, errors = sys.makeOrder(orderedFood)
	order = sys.makeOrder()
	print(order._orderStatus)
	testGet = sys.getNextOrder('Not Submitted')

	assert(testGet == order)

# def test_getNextOrder_with_multiple_orders(sys):
# 	orderedFood1 = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
# 	burger = sys.getFood('Burger')
# 	burger.addBuns(3)
# 	burger.addPats(2)
# 	burger.changeIngredients('tomato', 2)
# 	burger.changeIngredients('cheddar_cheese', 3)
# 	orderedFood2 = {burger: 1, sys.getFood('Orange_Juice','sml'): 2}
# 	order, errors = sys.makeOrder(orderedFood1)
# 	order2, errors = sys.makeOrder(orderedFood2)
# 	testGet = sys.getNextOrder('Pending')
# 	assert(testGet == order)
# 	order.updateOrder('someStat')
# 	testGet = sys.getNextOrder('someStat')
# 	assert(testGet == order)
# 	testGet = sys.getNextOrder('Pending')
# 	assert(testGet == order2)
# 	testGet = sys.getNextOrder(None,2)
# 	assert(testGet == order2)
# 	testGet = sys.getNextOrder(None,100)
# 	assert(testGet == None)

# def test_deleteOrder_if_id_not_found(sys):
# 	wrap = sys.getFood('Wrap')
# 	wrap.addPats(3)
# 	wrap.changeIngredients('tomato_sauce', 3)
# 	orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
# 	order, errors = sys.makeOrder(orderedFood)
# 	testDelete = sys.deleteOrder(None, 3)
# 	assert(testDelete == None)
# 	assert(len(sys.order) == 1)

# def test_deleteOrder_if_id_found(sys):
# 	wrap = sys.getFood('Wrap')
# 	wrap.addPats(3)
# 	wrap.changeIngredients('tomato_sauce', 3)
# 	orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
# 	order, errors = sys.makeOrder(orderedFood)
# 	testDelete = sys.deleteOrder(None, 1)
# 	assert(testDelete == order)
# 	assert(len(sys.order) == 0)

# def test_deleteOrder_if_stat_not_found(sys):
# 	wrap = sys.getFood('Wrap')
# 	wrap.addPats(3)
# 	wrap.changeIngredients('tomato_sauce', 3)
# 	orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
# 	order, errors = sys.makeOrder(orderedFood)
# 	testDelete = sys.deleteOrder('someStat')
# 	assert(testDelete == None)
# 	assert(len(sys.order) == 1)

# def test_deleteOrder_if_stat_found(sys):
# 	wrap = sys.getFood('Wrap')
# 	wrap.addPats(3)
# 	wrap.changeIngredients('tomato_sauce', 3)
# 	orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
# 	order, errors = sys.makeOrder(orderedFood)
# 	testDelete = sys.deleteOrder('Pending')
# 	assert(testDelete == order)
# 	assert(len(sys.order) == 0)

# def test_delete_multiple_orders(sys):
# 	orderedFood1 = {sys.getFood('Nuggets','sml'): 3, sys.getFood('Lemonade', 'Cans'): 3}
# 	burger = sys.getFood('Burger')
# 	burger.addBuns(3)
# 	burger.addPats(2)
# 	burger.changeIngredients('tomato', 2)
# 	burger.changeIngredients('cheddar_cheese', 3)
# 	orderedFood2 = {burger: 1, sys.getFood('Orange_Juice','sml'): 2}
# 	order, errors = sys.makeOrder(orderedFood1)
# 	order2, errors = sys.makeOrder(orderedFood2)
# 	testDelete = sys.deleteOrder('something')
# 	assert(testDelete == None)
# 	assert(len(sys.order) == 2)
# 	order.updateOrder('someStat')
# 	testDelete = sys.deleteOrder('someStat')
# 	assert(testDelete == order)
# 	assert(len(sys.order) == 1)
# 	testDelete = sys.deleteOrder(None,2)
# 	assert(testDelete == order2)
# 	assert(len(sys.order) == 0)
