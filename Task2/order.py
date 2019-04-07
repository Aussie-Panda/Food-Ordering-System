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
    
