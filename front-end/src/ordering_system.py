from src.food import Food
from src.order import Order
from src.stock import Stock
from src.errors import StockError, bun_error, check_numBuns_error, checkStock
from src.mains import Mains, Burger, Wrap
from src.drinks import Drinks
from src.sides import Sides

class OrderingSystem():
    def __init__(self):
        self._id = 0
        self._order = []            # a list of Order. order's id should be in increasing order
        self._mainsMenu = []        # a list of Mains
        self._drinksMenu = []       # a list of drinks
        self._sidesMenu = []        # a list of sides
        self._stock = Stock()

    def newId(self):
        self._id += 1
        return self._id

    def displayMenu(self):
        print("--------MENU--------")
        print("  ---Mains Menu---")
        for item in self.mainsMenu:
            print(item)

        print(" ---Drinks Menu---")
        for item in self.drinksMenu:
            print(item)

        print(" ---Sides Menu---")
        for item in self.sidesMenu:
            print(item)

        print("-------End of Menu-------")

    # pass in str and get food instance from menu
    # size: str (sml, med, lrg, Bottles, Cans)
    # name: str
    def getFood(self,name,size=None):
        target = None

        # Mains dont have size
        if size == None:
            for i in self.mainsMenu:
                if i.name == name:
                    target = i

        # Drinks and Sides have size
        if size != None:
            for menu in [self.drinksMenu,self.sidesMenu]:
                for i in menu:
                    if i.name == name and i.size == size:
                        target = i

        return target



    '''
    Check if item in food is out of stock. If yes, raise StockErrors; if no, create new order instance, 
    append it to order list and set status as "Pending"
    food: a dictionary with key: instance of Food, value: int
    return value: Order or None

    Modified: don't need food, only need to create a new order and use modifyorder to add
    food
    '''
    def makeOrder(self):
        
        emptyFood = checkStock(food, self.stock)
        if emptyFood:
            raise StockError(emptyFood)
        
        else:
            newId = self.newId()
            new_order = Order(newId, food, "Pending")
            # print(new_order)
            self.order.append(new_order)
            price = new_order.computeNetPrice()

            # consume food
            self.stock.consumeFood(new_order.orderedItem)
            print(f"Thank you, your order has been made.\nTotal Price: ${price}")
            
            return new_order
            
    
    '''
    A function to add/modify the quantity of the food into the order list
    id is a int indicating the order you want to modified
    itemList is a list of food string (input from flask)
    value is the amount of the food you want
    '''
    def modifyOrder(self, id, itemList, value):
        #get the order that want to be modified
        order = self.getNextOrder(None,id)
        for food in itemList:
            food = self.getFood(food)









    '''
    Generate receipt of an order
    order: an instance of Order
    return value: string
    '''
    def printReceipt(self,order):
        assert(order != None)
        
        receipt = f'---------Receipt--------\n{order}\n--------End of Receipt--------'
        return receipt


    '''
    Get next order either by status or particular id.
    status: string, id: int
    return value: order (if found)/None(if not found)
    '''
    def getNextOrder(self, status = None, id = None):

        if id is None:
            for i in self.order:
                if i.orderStatus == status:
                    return i

        elif id is not None:
            for i in self.order:
                if i.orderId == id:
                    return i

        return None     # if no order matches the requesting status or id

    '''
    Delete the next order that has requesting status or particular id
    status: string, id: int
    return value: order (if found)/None(if not found)
    '''
    def deleteOrder(self, status = None, id = None):

        if id is None:
            for i in self.order:
                if i.orderStatus == status:
                    self.order.remove(i)
                    return i

        elif id is not None:
            for i in self.order:
                if i.orderId == id:
                    self.order.remove(i)
                    return i

        return None     # if no order matches the requesting status or id
        

    '''
    Properties
    '''

    @property
    def order(self):
        return self._order

    
    @property
    def mainsMenu(self):
        return self._mainsMenu
    
    @property
    def drinksMenu(self):
        return self._drinksMenu
    
    @property
    def sidesMenu(self):
        return self._sidesMenu
    
    @property
    def stock(self):
        return self._stock
    
    @mainsMenu.setter
    def mainsMenu(self, new):
        self._mainsMenu = new
        
    @drinksMenu.setter
    def drinksMenu(self, new):
        self._drinksMenu = new
    
    @sidesMenu.setter
    def sidesMenu(self, new):
        self._sidesMenu =  new
        
