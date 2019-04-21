from src.food import Food
from src.mains import Mains, Burger, Wrap
from src.errors import StockError, SearchError
import copy

class Order():
    def __init__(self, orderId, orderStatus = "Not Submitted"):
        self._orderId = int(orderId)         # int
        self._orderedItem = {}          # a dictionary, key=Food, value=int
        self._orderStatus = orderStatus # string

    '''
    get a particular food from the order, raise Error if not found
    name: str, size = str
    return value: the instance or Food (if found)
    '''
    def getFood(self,name,size=None):
        target = None
        for i in self.orderedItem:
            if isinstance(i, Mains):
                if i.name == name:
                    target = i
            else:
                if i.name == name and i.size == size:
                    target = i
        # is not found, raise SearchError
        if target is None:
            raise SearchError(Food)
        else:
            return target
        
    # compute total price of the order
    # need to be change if Burger and wrap is ready.
    def computeNetPrice(self):
        totalPrice = 0
        thisPrice = 0
        for item in self.orderedItem.keys():

            if isinstance(item, Mains):
                thisPrice = item.computePrice()
            else:
                thisPrice = item.price
            
            quantity = self.orderedItem[item]
            totalPrice += (thisPrice * quantity)

        return totalPrice


    # update orderStatus, raise Error if the input status is not valid
    def updateOrder(self, status):
        if (status != 'Not Submitted' and status != 'Pending' and status != 'Preparing' and status != 'Ready' and status != 'Picked Up'):
            raise Exception("Invalid Status Input")
        else:
            self._orderStatus = status
        
   
    '''
    method to add food into order
    item: an new instance of food
    '''
    def addFood(self, item, value):
        assert (value > 0)
        try:
            size = item.size
        
        except:
            self.orderedItem[item] = value
            
        else:
            try:
                food = self.getFood(item.name, size)
            except SearchError:
                self.orderedItem[item] = value
            else:
                self.orderedItem[food] += value
    '''
    method to delete food from order
    item: an instance from orderedItem
    '''
    def deleteFood(self, item):
        self.orderedItem.pop(item)

    # to print out the order detail
    def __str__(self):
        price = self.computeNetPrice()
        msg = ""
        msg += f"Order id: {self._orderId}\n\n"
        msg += "Order items:\n"
        for i in self._orderedItem.keys():
            quantity = str(self._orderedItem[i])
            msg += f"{i} * {quantity}\n"
        msg += f"\nOrder status: {self._orderStatus}\n\n"
        msg += f"Total Price: ${price}"
        return msg


    ''' 
    Properties
    '''

    @property
    def orderId(self):
        return self._orderId
    
    @property
    def orderedItem(self):
        return self._orderedItem
    
    @property
    def orderStatus(self):
        return self._orderStatus
    
