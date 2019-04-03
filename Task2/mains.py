
#created by Yanning Cao from memberless Team
#mains class
from food import Food

class Mains(Food):  

    def __init__(self, name, price):
        super().__init__(name, price)
        #dictionary of ingredient that have been ordered
        self._ingredientsOrdered = {}
        self._ingredientsMenu = {'tomato': 1, 'lettuce' : 1, 'cheddar_cheese' : 2, 'swisse_cheese' : 3, 'tomato_sauce' : 1}
    
    #getters and setters
    @property
    def ingredientsOrdered(self):
        return self._ingredientsOrdered

    @property
    def ingredientsMenu(self):
        return self._ingredientsMenu

    #method can be add or delete ingridient is one of the elem in the list
    def changeIngredients(self, ingredient, amount = None):
        #check inputs
        assert(ingredient != None)
        assert(amount != None)
        
        #change the amoun of the ingredient
        self.ingredientsOrdered[ingredient] = amount
        
    
    def computePrice(self):
        pass

class Burger(Mains):

    def __init__(self, numBun, numPat):
        super().__init__('Burger', 5)
        self._numBun = numBun
        self._numPat = numPat
        self._bunPrice = 1
        self._patPrice = 2

    def computePrice(self):
        burger_price = self._price + self._numBun * self._bunPrice + self._numPat * self._patPrice
        ingridient_price = 0
        for elem in self.ingredientsOrdered.keys():
            ingridient_price += self.ingredientsOrdered[elem] * self.ingredientsMenu[elem]
        total = ingridient_price + burger_price
        return total


class Wrap(Mains):

    def __init__(self,numPat):
        super().__init__('Wrap',4)
        self._numPat = numPat
        self._patPrice = 2

    def computePrice(self):
        total = self._price + self._numPat * self._patPrice
        ingridient_price = 0
        for elem in self.ingredientsOrdered.keys():
            ingridient_price += self.ingredientsOrdered[elem] * self.ingredientsMenu[elem]
        total += ingridient_price
        return total



'''
# For simple testing
m1 = Mains('shit',9999999999)
m1.changeIngredients('shit',99)
print(m1.name)
print(m1.price)
'''

#test burgers and wraps
bug = Burger(2,2)
print(bug._name)
print(bug._price)
bug.changeIngredients('tomato', 10)
price = bug.computePrice()
print(price)

wrap = Wrap(2)
wrap.changeIngredients('lettuce', 10)
price2 = wrap.computePrice()
print(price2)



