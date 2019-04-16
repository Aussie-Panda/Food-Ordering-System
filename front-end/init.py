from src.ordering_system import OrderingSystem
from src.food import Food
from src.order import Order
from src.stock import Stock
from src.errors import StockError, bun_error, check_numBuns_error, checkStock
from src.mains import Mains, Burger, Wrap
from src.drinks import Drinks
from src.sides import Sides


def bootstrap_system():
    system = OrderingSystem()
    
    # initialise menu
    # Mains Burger(numBun, numPat) Wrap(numPat)
    mains = [
        Burger('Burger', 5),
        Wrap('Wrap', 4),
    ]
    

    # Drinks(name, price, size, volumn)
    drinks = [
        Drinks('Lemonade', 3, 'Cans', 375, 'ml'),
        Drinks('Lemonade', 5, 'Bottles', 600, 'ml'),
        Drinks('Orange_Juice', 2, 'sml', 250, 'ml'),
        Drinks('Orange_Juice', 4, 'med', 450, 'ml'),
    ]

    # Sides(self, name, price, size, type)
    sides = [
        Sides('Nuggets', 1, 'sml', 3, '/pack'),
        Sides('Nuggets', 2, 'lrg', 6, '/pack'),
        Sides('Fries', 1, 'sml', 20, 'g'),
        Sides('Fries', 2, 'med', 40, 'g'),
        Sides('Fries', 3, 'lrg', 60, 'g'),
    ]

    for f in mains:
        system.addFood(system.mainsMenu,f)

    for f in drinks:
        system.addFood(system.drinksMenu,f)

    for f in sides:
        system.addFood(system.sidesMenu, f)

    # initialise stock
    for category in [system.stock.mains, system.stock.drinks, system.stock.sides, system.stock.ingredients]:
        for item in category:
            if item == 'Fries':
                category[item] = 10000
            elif 'Juice' in item:
                category[item] = 100000
            else:
                category[item] = 100
    
    return system
