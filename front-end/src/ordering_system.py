from src.food import Food
from src.order import Order
from src.stock import Stock
from src.errors import StockError, SearchError
from src.mains import Mains, Burger, Wrap
from src.drinks import Drinks
from src.sides import Sides
import copy

class OrderingSystem():
    def __init__(self):
        self._id = 0
        self._order = []            # a list of Order. order's id should be in increasing order
        # self._category = ['Mains': self._mainsMenu, 'Drinks': self._drinksMenu, 'Sides': self._sidesMenu]
        self._mainsMenu = []        # a list of Mains
        self._drinksMenu = []       # a list of drinks
        self._sidesMenu = []        # a list of sides
        self._stock = Stock()
        self._statusList = ['Not Submitted', 'Pending', 'Preparing', 'Ready', 'Picked Up']

    def newId(self):
        self._id += 1
        return self._id

    # add food into category, food: food instance
    def addFood(self, category,food):
        assert(food != None)
        if category in [self.mainsMenu, self.sidesMenu, self.drinksMenu]:
            category.append(food)
        else:
            raise Exception('No such menu')

    # pass in str and get food instance from menu
    # size: str (sml, med, lrg, Bottles, Cans)
    # name: str
    # Will raise SearchError if Food is not found
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
        # if not found, raise SearchError
        if target is None:
            raise SearchError(f"{name}")
        else:
            return target


    '''
    make a new order once the customer enter the menu page. This will be appended to order list
    '''
    def makeOrder(self):
        
        newId = self.newId()
        new_order = Order(newId, "Not Submitted")
        # print(new_order)
        self.order.append(new_order)

        return new_order
    
    '''
    Check if item in food is out of stock. If yes, raise StockErrors; if no, append it to order list and set status as "Pending"
    order: an Order instance
    return value: Order or None
    Will raise StockError if some food is out of stock
    '''
    def confirmOrder(self, order):
        
        emptyFood = self.checkStock(order.orderedItem, self.stock)
        if emptyFood:
            raise StockError(emptyFood)
        
        else:
            order.updateOrder("Pending")
            # print(order)
            # consume food
            self.consumeFood(order.orderedItem)
            
            return order
    
    # consume food from stock
    def consumeFood(self, food):
        for item in food:
            self.stock.decreaseQuantity(item, food[item])

            # for Mains, should further find out how many buns/patties/ingradients are consumed
            if isinstance(item, Mains):
                # subtract addOn quantity by standard mains's addOn quantity
                standard = self.getFood(item.name)

                for i in item.ingredientsOrdered.keys():
                    self.stock.decreaseQuantity(i, item.ingredientsOrdered[i]) 
                for a in item.addOn.keys():
                    aL = a.lower()
                    quantity = item.addOn[a] - standard.addOn[a]
                    self.stock.decreaseQuantity(aL, quantity)

    '''
    Get next order either by status or particular id.
    status: string, id: int
    return value: order (if found)/None(if not found)
    Will raise Error if order not found
    '''
    def getNextOrder(self, status = None, id = None):
        target = None
        # get order by status
        if id is None:
            for i in self.order:
                if i.orderStatus == status:
                    target = i

        # get order by id
        elif id is not None:
            id = int(id)
            for i in self.order:
                if i.orderId == id:
                    target = i

        if target is None:
            raise SearchError('Order')
        else:
            return target     # if no order matches the requesting status or id

    '''
    Delete the next order that has requesting status or particular id
    status: string, id: int
    return value: order (if found)/None(if not found)
    '''
    def deleteOrder(self, id):
        for i in self.order:
            if i.orderId == id:
                self.order.remove(i)
                return i


        raise SearchError("Order")     # if no order matches the requesting status or id


    # to catch a list of order by status
    def filterOrder(self, statusList):
        NotSubmitted = ['Not Submitted']
        Pending = ['Pending']
        Preparing = ['Preparing']
        Ready = ['Ready']
        PickedUp = ['Picked Up']
        for order in self.order:
            for label in [NotSubmitted, Pending, Preparing, Ready, PickedUp]:
                if order.orderStatus == label[0]:
                    label.append(order)
                    break

        returnList = []
        for label in [NotSubmitted, Pending, Preparing, Ready, PickedUp]:
            if label[0] in statusList:
                returnList += label[1:]

        return returnList

    '''
    Check if a dictionary of food is out of stock
    return value: a list of out-of-stock food
    '''
    def checkStock(self, food, stock):
        emptyFood = []
        totalFood = {}
        # calculate total quantity/volumn for each type of food
        for item in food.keys():
            # for mains
            if isinstance(item, Mains):
                # only addtional addOn need to be consumed seperatly
                standard = self.getFood(item.name)

                totalFood[item.name] = food[item]
                for addOn in item.addOn.keys():
                    if addOn not in totalFood:
                        totalFood[addOn.lower()] = (item.addOn[addOn] - standard.addOn[addOn])
                    else:
                        totalFood[addOn.lower()] += (item.addOn[addOn] - standard.addOn[addOn])

                for i in item.ingredientsOrdered.keys():
                    totalFood[i] = item.ingredientsOrdered[i]

            # for drinks
            elif isinstance(item, Drinks):
                if 'Juice' in item.name:
                    totalFood[item.name] = food[item] * item.volumn
                else:
                    target = f"{item.name}({item.size})"
                    totalFood[target] = food[item]

            # for sides
            elif isinstance(item, Sides):
                if item.name not in totalFood:
                    totalFood[item.name] = food[item] * item.volumn
                elif item.name in totalFood:
                    totalFood[item.name] += food[item] * item.volumn

        # print(totalFood)
        for item in totalFood.keys():
            for category in stock.whole.values():
                if (item in category) and (category[item] < totalFood[item]):
                    emptyFood.append(item)
        
        return emptyFood

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
    
    @property
    def statusList(self):
        return self._statusList
    
    '''
    setters
    '''
    
    @mainsMenu.setter
    def mainsMenu(self, new):
        self._mainsMenu = new
        
    @drinksMenu.setter
    def drinksMenu(self, new):
        self._drinksMenu = new
    
    @sidesMenu.setter
    def sidesMenu(self, new):
        self._sidesMenu =  new
        
