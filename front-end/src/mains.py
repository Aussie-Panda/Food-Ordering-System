#created by Yanning Cao from memberless Team
#mains class
from src.food import Food

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

    def __init__(self,name, price):
        super().__init__(name,price)
        self._numBun = 0
        self._numPat = 0
        self._bunPrice = 1
        self._patPrice = 2

    def computePrice(self):
        burger_price = self._price + self._numBun * self._bunPrice + self._numPat * self._patPrice
        ingridient_price = 0
        for elem in self.ingredientsOrdered.keys():
            ingridient_price += self.ingredientsOrdered[elem] * self.ingredientsMenu[elem]
        total = ingridient_price + burger_price
        return total

    def addBuns(self, amount):
        self._numBun += amount

    def addPats(self, amount):
        self._numPat += amount

    @property
    def numBun(self):
        return self._numBun
     
    @property
    def numPat(self):
        return self._numPat
        

    def __str__(self): 
        msg = f"Buger: Buns * {self._numBun}, Patties * {self._numPat}.\n  Ingredients: "
        for elem in self.ingredientsOrdered.keys():
            msg += f"{elem} * {self.ingredientsOrdered[elem]}, "

        return msg


class Wrap(Mains):

    def __init__(self, name, price):
        super().__init__(name, price)
        self._numPat = 0
        self._patPrice = 2

    def computePrice(self):
        total = self._price + self._numPat * self._patPrice
        ingridient_price = 0
        for elem in self.ingredientsOrdered.keys():
            ingridient_price += self.ingredientsOrdered[elem] * self.ingredientsMenu[elem]
        total += ingridient_price
        return total

    def addPats(self, amount):
        self._numPat += amount
        
    @property
    def numPat(self):
        return self._numPat
    
    def __str__(self): 
        msg = f"Wrap: Patties * {self._numPat}.\n  Ingredients: "
        for elem in self.ingredientsOrdered.keys():
            msg += f"{elem} * {self.ingredientsOrdered[elem]}, "

        return msg

