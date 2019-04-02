from Food import Food
from order import Order
from stock import Stock


class IdGenerator():

	def __init__(self):
		self._id = 0

	def newId(self):
		self._id += 1
		return self._id

class OrderingSystem():
	def __init__(self):
		self._order = []	# order's id should be in increasing order
		self._menu = []		# a list of all kind food


	def displayMenu(self):
		for item in self.menu:
			print(item)

	'''
	Function to make new order.
	1. If no existed order passed in, make new one and checkStock. If some items are out of stock, return the order and set orderStatus as "Not Submitted", else, append it to order list and set status "Pending"
	2. If an old order passed in, re-check stock. If there are still some items out of stock, return order; else, append it to order list and update status "Pending"

	return value: order
	'''
	def makeOrder(self, old_order = None, food = None):
		
		assert(food != None)

		if order==None:
			newId = IdGenerator.newId()
			emptyFood = checkStock(food)
			if emptyFood:
				new_order = Order(newID,food,"Not Submitted")
			else:
				new_order = Order(newID, food, "Pending")
				self.order.append(new_order)
				
			return new_order

		else:
			assert(old_order != None)
			emptyFood = checkStock(food)
			if emptyFood:
				old_order.modifyOrder(food)
			else:
				old_order.modifyOrder(food)
				order.updateOrder("Pending")
				self.order.append(old_order)

			return old_order
			
	'''
	Check if a list of food is out of stock
	return value: list of out-of-store food
	'''
	def checkStock(self, order):
		emptyFood = []

		for item in order.orderedItem:
			if item in Stock.mains:
				if Stock.mains[item] == 0:
					emptyFood.append(item)

			elif item in  Stock.drinks:
				if Stock.drinks[item] == 0:
					emptyFood.append(item)

			elif item in Stock.sides:
				if Stock.sides[item] == 0:
					emptyFood.append(item)

			elif item in Stock.ingredients:
				if Stock.ingredients[item] == 0:
					emptyFood.append(item)

		return emptyFood


	'''
	Ask for customer if they would like to enter email address and then send a receipt
	return value: None (void function)
	'''
	def sendReceipt(self,order):
		assert(order != None)
		send = input("Would you like to send a receit? (y/n): ")
		food = '\n'.join(order.orderedItem)
		receipt = f'----------\nDear customer,\nYour order has been confirmed.\nYour order ID is: {order.orderId}\nYour items are: \n{food}\n\nThank you for ordering!\n----------'

		if send == 'y':
			email = ""
			email += input("Please enter your email: ")
			if email:
				print("Your receipt has been sent to email " + email)
				print(receipt)

			elif not email:
				print(receipt)


	'''
	Get next order either by status or particular id.
	return value: order (if found)/None(if not found)
	'''
	def getNextOrder(self, status = None, id = None):
		assert(status != None)

		if id is None:
			for i in self.order:
				if i.order.orderStatus == status:
					return i

		elif id is not None:
			for i in self.order:
				if i.order.orderId == id:
					return i

			return None		# if no order matches the requesting status or id

	'''
	Delete the next order that has requesting status or id
	return value: order (if found)/None(if not found)
	'''
	def deleteOrder(self, status = None, id = None):

		if status is not None and id is None:
			for i in self.order:
				if i.order.orderStatus == status
					self.order.remove(i)
					return i

		elif status is not None and id is not None:
			for i in self.order:
				if i.order.orderStatus == status and i.order.orderId == id:
					self.order.remove(i)
					return i

		elif status is None and id is not None:
			for i in self.order:
				if i.order.orderId == id:
					self.order.remove(i)
					return i

		return None		# if no order matches the requesting status or id
		


	'''
	Properties
	'''

	@property
	def order(self):
		return self._order

	
	@property
	def menu(self):
		return self._menu
	