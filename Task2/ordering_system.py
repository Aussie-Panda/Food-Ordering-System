from food import Food
from order import Order
# from stock import Stock
from errors import StockError, QuantityError, checkStock
from mains import Mains, Burger, Wrap


class OrderingSystem():
    def __init__(self):
        self._id = 0
        self._order = []    # a list of Order. order's id should be in increasing order
        self._mainsMenu = []        # a list of Mains
        self._drinksMenu = []       # a list of drinks
        self._sidesMenu = []        # a list of sides

    def newId(self):
        self._id += 1
        return self._id

    def displayMenu(self):
        print("--------MENU--------")
        for item in self.menu:
            print(item)
        print("-------End of Menu-------")

    def getFood(self,name):
        target = None
        for i in self.mainsMenu:
            if i.name == name:
                target = i

        if taret == None:
            for i in self.drinksMenu:
                if i.name == name:
                    target = i

        if target == None:
            for i in self.sidesMenu:
                if i.name == name:
                    target = i

        return target

    def initMenu(self):
        # Mains Burger(numBun, numPat) Wrap(numPat)
        burger = Burger(0, 0)
        wrap = Wrap(0)

        # Drinks(name, price, volume, type)
        can = Drinks('Can', 3, 375, 'Drinks')
        bottles = Drinks('Bottles', 5, 600, 'Drinks')
        smlJuice = Drinks('smlJuice', 2, 250, 'Drinks')
        medJuice = Drinks('medJuice', 4, 450, 'Drinks')

        # Sides(self, name, price, size, type)
        smlNuggets = Sides('Nuggets', 1, 'sml', 'Sides')
        lrgNuggets = Sides('Nuggets', 2, 'lrg', 'Sides')
        smlFries = Sides('Fries', 1, 'sml', 'Sides')
        medFries = Sides('Fries', 2, 'med', 'Sides')
        lrgFries = Sides('Fries', 3, 'lrg', 'Sides')


        self._mainsMenu = [burger, brap]
        self._drinksMenu = [can, bottles, smlJuice, medJuice]
        self._sidesMenu = [smlNuggets, lrgNuggets, smlFries, medFries, lrgFries]

    '''
    Check if item in food is out of stock. If yes, return None and errors; if no, create new order instance, 
    append it to order list and set status as "Pending"
    return value: order, [](if no StockError)/None, error list(if StockError)
    '''
    def makeOrder(self, food = None):
        
        assert(food != None)

        '''
        try:
            checkStock(food)

        except StockError as er:
            return None, er.errors
        '''
        newId = self.newId()
        new_order = Order(newId, food, "Pending")
        # print(new_order)
        self.order.append(new_order)
        
        price = new_order.computeNetPrice()
        print(f"Thank you, your order has been made.\nTotal Price: ${price}")
        
        return new_order, []
            


    # Funciton to modify the tmp order
    def modifyOrder(self, food=None, item=None, value=None):
        assert(food != None)
        assert(item != None)
        assert(value != None)


        # If any invalid value is passed in, raise QuantityError. Errors should be catched outside
        if value < 0:
            return None,[];
            
        # 1. if item is in the order and value is set to 0, delete the item
        # 2. elif item is in the list and value is > 0, overwrite the previous value
        elif item in food:
            if value == 0:
                food.pop(item)
            else:
                food[item] = value

        # 3. elif item is not in the list, add item with value
        elif item not in food:
            # if customer enter value 0, do nothing
            if value != 0:
                food[item] = value
        try:
            checkStock(food)  
        except StockError as er:
            return None, er.errors


        return food, []           

    '''
    Ask for customer if they would like to enter email address and then send a receipt
    return value: None (void function)
    '''
    def sendReceipt(self,order):
        assert(order != None)
        send = 'n'
        # send = input("Would you like to send a receit? (y/n): ")
        '''
        price = order.computeNetPrice
        receipt = f'------Receipt-----\nDear customer,\nYour order has been confirmed.\nYour order ID is: {order.orderId}\nYour items are: \n{food}\nTotal Price: ${price}\nThank you for ordering!\n--------End of Receipt-------'
        '''
        receipt = f'---------Receipt--------\n{order}\n--------End of Receipt--------'
        if send == 'y':
            email = ""
            email += input("Please enter your email: ")
            
            while not email:
                email += input("Please enter your email: ")

            
            print("Your receipt has been sent to email " + email)
            print(receipt)


        else:
            print(receipt)


    '''
    Get next order either by status or particular id.
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
    

sys = OrderingSystem()
sys.initMenu()
sys.displayMenu
