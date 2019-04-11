from food import Food
from mains import Mains, Burger, Wrap

class Order():
    def __init__(self, orderId, food, orderStatus = "Not Submitted"):
        self._orderId = orderId         # int
        self._orderedItem = food        # a dictionary, key=Food, value=int
        self._orderStatus = orderStatus # string

    # get a particular food from the order
    # name: str, size = str
    # return value: the instance or Food (if found)/ None(if not found)
    def getFood(self,name,size=None):
        for i in self.orderedItem:
            if isinstance(i, Mains):
                if i.name == name:
                    return i
            else:
                if i.name == name and i.size == size:
                    return i
        return None

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



    # update orderStatus
    def updateOrder(self, status):
        self._orderStatus = status
        
    def __str__(self):
        price = self.computeNetPrice()
        msg = ""
        msg += f"Order id: {self._orderId}\n"
        msg += "Order items:\n"
        for i in self._orderedItem.keys():
            quantity = str(self._orderedItem[i])
            msg += f"{i} * {quantity}\n"
        msg += f"Order status: {self._orderStatus}\n"
        msg += f"Total Price: ${price}"
        return msg

        
    '''
    Method to modify the order
    food: a dictionary with key: instance of Food, value: int;
    item: instance of food;
    value: int.
    return value:None
    '''
    def modify(self, item=None, value=None):
        assert(item != None)
        assert(value != None)
        
        # If any invalid value is passed in, return None and empty error list
        if value < 0:
            return None,[]
            
        # 1. if item is in the order and value is set to 0, delete the item
        # 2. elif item is in the list and value is > 0, overwrite the previous value
        elif item in self.orderedItem:
            if value == 0:
                self.orderedItem.pop(item)
            else:
                self.orderedItem[item] = value

        # 3. elif item is not in the list, add item with value
        elif item not in self.orderedItem:
            # if customer enter value 0, do nothing
            if value != 0:
                self.orderedItem[item] = value
        

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
    
