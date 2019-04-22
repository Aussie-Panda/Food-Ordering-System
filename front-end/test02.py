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
import copy

@pytest.fixture
def sys():
	sys = bootstrap_system()
	return sys


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

def test_deleteOrder_if_id_not_found(sys):
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
	testDelete = None
	try:
		testDelete = sys.deleteOrder(3)
	except SearchError as er:
		assert(True)
	assert(testDelete == None)
	assert(len(sys.order) == 1)

def test_deleteOrder_if_id_found(sys):
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
	testDelete = None
	testDelete = sys.deleteOrder(1)
	assert(testDelete == order)
	assert(len(sys.order) == 0)

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

def test_filterOrder(sys):
	list1 = ['Pending']
	list2 = ['Ready']
	list3 = ['Pending','Ready']
	order1 = sys.makeOrder()
	wrap = sys.getFood('Wrap')
	wrap.addOn['Patties'] = 3
	wrap.changeIngredients('tomato_sauce', 3)
	order1.addFood(wrap,1)
	fries = sys.getFood('Fries', 'lrg')
	# orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
	# order.addFood(wrap,1)
	order1.addFood(fries,1)
	sys.confirmOrder(order1)

	order = sys.makeOrder()
	burger = sys.getFood('Burger')
	burger.addOn['Buns'] = 3
	burger.addOn['Patties'] = 2
	burger.changeIngredients('tomato', 2)
	burger.changeIngredients('cheddar_cheese', 3)
	order.addFood(burger,1)
	sys.confirmOrder(order)

	order3 = sys.makeOrder()
	nuggets = sys.getFood('Nuggets','sml')
	lemon = sys.getFood('Lemonade', 'Cans')
	order3.addFood(nuggets,3)
	order3.addFood(lemon,3)
	sys.confirmOrder(order3)
	order3.updateOrder('Ready')
	res = sys.filterOrder(list1)
	assert(len(res) == 2)
	res2 = sys.filterOrder(list2)
	assert(len(res2) == 1)
	res = sys.filterOrder(list3)
	assert(len(res) == 3)