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
	assert(testMains.price == 3)
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
	assert(sys.stock.sides['Nuggets'] == 991)
	assert(sys.stock.drinks['Lemonade(Cans)'] == 997 )

def test_make_order_default_buger(sys):
	order = sys.makeOrder()
	burger = sys.getFood('Burger')
	# burger.addOn['Buns'] = 3
	# burger.addOn['Patties'] = 2
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
	assert(order.computeNetPrice() == 19)

def check_stock_after_making_std_order(sys):
	order = sys.makeOrder()
	burger = sys.getFood('Burger')
	# burger.addOn['Buns'] = 3
	# burger.addOn['Patties'] = 2
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
	assert(sys.stock.drinks['Orange_Juice'] == 500)
	assert(sys.stock.ingredients['tomato'] == 98)
	assert(sys.stock.ingredients['cheddar_cheese'] == 97)
	assert(sys.stock.ingredients['buns'] == 100)
	assert(sys.stock.ingredients['patties'] == 100)
	assert(sys.stock.mains['Burger'] == 99)

def test_make_order_customize_buger(sys):
	order = sys.makeOrder()
	burger2 = sys.getFood('Burger')
	burger = copy.deepcopy(burger2)
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
	assert(order.computeNetPrice() == 22)


def test_check_stock_after_making_customiz_order(sys):
	order = sys.makeOrder()
	burger2 = sys.getFood('Burger')
	burger = copy.deepcopy(burger2)
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

	assert(sys.stock.drinks['Orange_Juice'] == 500)
	assert(sys.stock.ingredients['tomato'] == 98)
	assert(sys.stock.ingredients['cheddar_cheese'] == 97)
	assert(sys.stock.ingredients['buns'] == 99)
	assert(sys.stock.ingredients['patties'] == 99)
	assert(sys.stock.mains['Burger'] == 99)

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
	assert(order.computeNetPrice() == 14)

	assert(sys.stock.sides['Fries'] == 940)
	assert(sys.stock.mains['Wrap'] == 99)
	assert(sys.stock.ingredients['tomato_sauce'] == 97)

def test_check_stock_if_out_of_stock(sys):
	order = sys.makeOrder()
	wrap2 = sys.getFood('Wrap')
	wrap = copy.deepcopy(wrap2)
	wrap.addOn['Patties'] = 30000
	wrap.changeIngredients('tomato_sauce', 3)
	order.addFood(wrap,1)
	fries = sys.getFood('Fries', 'lrg')
	# orderedFood = {wrap: 1, sys.getFood('Fries', 'lrg'): 1}
	# order.addFood(wrap,1)
	order.addFood(fries,1)
	try:
		sys.confirmOrder(order)
	except StockError as er:
		assert(True)
	else:
		assert(False)
