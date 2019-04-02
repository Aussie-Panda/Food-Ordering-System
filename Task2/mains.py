
#created by Yanning Cao from memberless Team
#mains class
from food import Food

class Mains(Food):  

    def __init__(self, name, price):
        super().__init__(name, price)
        #list of ingredient that have been ordered
        self._ingredients = {}

    
    #getters and setters
    @property
    def ingredients(self):
        return self._ingredients

    #method can be add or delete ingridient is one of the elem in the list
    def changeIngredients(self, ingredient, amount = None):
        #check inputs
        assert(ingredient != None)
        assert(amount != None)
        
        #change the amoun of the ingredient
        self.ingredients[ingredient] = amount
        
    def computePrice(self):
        pass


'''
# For simple testing
m1 = Mains('shit',9999999999)
m1.changeIngredients('shit',99)
print(m1.name)
print(m1.price)
'''