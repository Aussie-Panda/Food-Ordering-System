from food import Food
from order import Order
from stock import Stock
from errors import StockError, QuantityError, checkStock
from mains import Mains, Burger, Wrap
from drinks import Drinks
from sides import Sides

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

    def initMenu(self):
        # Mains Burger(numBun, numPat) Wrap(numPat)
        burger = Burger('Burger',5)
        wrap = Wrap('Wrap',4)

        # Drinks(name, price, size, volumn)
        can = Drinks('Lemonade', 3, 'Cans', 375)
        bottles = Drinks('Lemonade', 5, 'Bottles', 600)
        smlJuice = Drinks('Orange_Juice', 2, 'sml',250)
        medJuice = Drinks('Orange_Juice', 4, 'med', 450)

        # Sides(self, name, price, size, type)
        smlNuggets = Sides('Nuggets', 1, 'sml', 3)
        lrgNuggets = Sides('Nuggets', 2, 'lrg', 6)
        smlFries = Sides('Fries', 1, 'sml', 20)
        medFries = Sides('Fries', 2, 'med', 40)
        lrgFries = Sides('Fries', 3, 'lrg', 60)


        self._mainsMenu = [burger, wrap]
        self._drinksMenu = [can, bottles, smlJuice, medJuice]
        self._sidesMenu = [smlNuggets, lrgNuggets, smlFries, medFries, lrgFries]


    '''
    Check if item in food is out of stock. If yes, return None and errors; if no, create new order instance, 
    append it to order list and set status as "Pending"
    food: a dictionary with key: instance of Food, value: int
    return value: order, [](if no StockError)/None, error list(if StockError)
    '''
    def makeOrder(self, food = None):
        
        assert(food != None)

        try:
            checkStock(food, self.stock)

        except StockError as er:
            return None, er.errors
        
        newId = self.newId()
        new_order = Order(newId, food, "Pending")
        # print(new_order)
        self.order.append(new_order)
        price = new_order.computeNetPrice()

        # consume food
        for item in food:
            self.stock.decreaseQuantity(item, food[item])

            # for Mains, should further find out how many buns/patties/ingradients are consumed
            if isinstance(item, Mains):
                for i in item.ingredientsOrdered.keys():
                    self.stock.decreaseQuantity(i, item.ingredientsOrdered[i]) 

                if isinstance(item, Burger):
                    self.stock.decreaseQuantity('buns', item.numBun)
                    self.stock.decreaseQuantity('patties', item.numPat)
                elif isinstance(item, Wrap):
                    self.stock.decreaseQuantity('patties', item.numPat)


        print(f"Thank you, your order has been made.\nTotal Price: ${price}")
        
        return new_order, []
            

    '''
    Funciton to modify the tmp order
    food: a dictionary with key: instance of Food, value: int;
    item: instance of food;
    value: int.
    return value:None
    '''
    def modifyOrder(self, food=None, item=None, value=None):
        assert(food != None)
        assert(item != None)
        assert(value != None)

        # If any invalid value is passed in, return None and empty error list
        if value < 0:
            return None,[]
            
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
    
'''

sys = OrderingSystem()
sys.initMenu()
sys.displayMenu()
print("Fries Storage:", sys.stock.sides['Fries'])
print("Nuggets Storage:", sys.stock.sides['Nuggets'])

l = {}
food = sys.getFood("Fries", "lrg")
if food is not None:
    l[food] = 3
food = sys.getFood("Nuggets", "sml")
if food is not None:
    l[food] = 4

print("you are ordering: ")
for i in l:
    print(i)

order, errors = sys.makeOrder(l)
if order:
    sys.sendReceipt(order)
print("Fries Storage:", sys.stock.sides['Fries'])
print("Nuggets Storage:", sys.stock.sides['Nuggets'])
'''