class Mains():  #remeber to put food!!!!!!!!!!!

    def __init__(self):

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
        
        self.ingredients[ingredient] = amount
        

m1 = Mains()
m1.changeIngredients('shit',99)
print(m1.ingredients)