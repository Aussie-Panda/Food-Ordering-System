#created by Yanning Cao from memberless Team
#mains class
from src.food import Food

class Mains(Food):  

    def __init__(self, name, price):
        super().__init__(name, price)
        #dictionary of ingredient that have been ordered
        self._ingredientsOrdered = {}
        self._ingredientsMenu = {'tomato': 1, 'lettuce' : 1, 'cheddar_cheese' : 2, 'swisse_cheese' : 3, 'tomato_sauce' : 1}
        self._addOnMenu = {'Buns': 1, 'Patties': 2}
    
    #getters and setters
    @property
    def ingredientsOrdered(self):
        return self._ingredientsOrdered

    @property
    def ingredientsMenu(self):
        return self._ingredientsMenu
    
    @property
    def addOnMenu(self):
        return self._addOnMenu
    
    @property
    def bunPrice(self):
        return self._addOnMenu['Buns']
    
    @property
    def patPrice(self):
        return self._addOnMenu['Patties']

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
        self._addOn = {'Buns': 0, 'Patties': 0}

    def computePrice(self):
        burger_price = self._price + self.numBun * self.bunPrice + self.numPat * self.patPrice
        ingridient_price = 0
        for elem in self.ingredientsOrdered.keys():
            ingridient_price += self.ingredientsOrdered[elem] * self.ingredientsMenu[elem]
        total = ingridient_price + burger_price
        return total

    @property
    def addOn(self):
        return self._addOn
    
    @property
    def numBun(self):
        return self._addOn['Buns']
    
    @property
    def numPat(self):
        return self._addOn['Patties']
    

    def __str__(self): 
        msg = f"Buger: (Buns * {self.numBun}, Patties * {self.numPat}. Ingredients: "
        for elem in self.ingredientsOrdered.keys():
            msg += f"{elem} * {self.ingredientsOrdered[elem]}, "
        msg += f') ${self.computePrice()}'
        return msg


class Wrap(Mains):

    def __init__(self, name, price):
        super().__init__(name, price)
        self._addOn = {'Patties': 0}
        self._numPat = 0

    def computePrice(self):
        total = self._price + self.numPat * self.patPrice
        ingridient_price = 0
        for elem in self.ingredientsOrdered.keys():
            ingridient_price += self.ingredientsOrdered[elem] * self.ingredientsMenu[elem]
        total += ingridient_price
        return total

    @property
    def addOn(self):
        return self._addOn
    
    @property
    def numPat(self):
        return self._addOn['Patties']
    
    def __str__(self): 
        msg = f"Wrap: (Patties * {self.numPat}. Ingredients: "
        for elem in self.ingredientsOrdered.keys():
            msg += f"{elem} * {self.ingredientsOrdered[elem]}, "
        msg += f') ${self.computePrice()}'
        return msg


