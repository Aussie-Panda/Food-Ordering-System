# import Flask library
from flask import Flask, render_template, request, redirect, url_for, abort, Markup,session, make_response
from init import bootstrap_system#, ser, orders
from src.errors import StockError, SearchError, bun_error, check_numBuns_error, checkStock
from src.shoppingCart import Cart
import copy

OVER_WRITE = True

# create a flask project, assigning to a variable called app
app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy

system = bootstrap_system()
# Loads data
orders = {}

# take in a Mains instance and extract information.
# info = {[item]: price}
def formatMains(food):
    info = {}
    try:
        target = system.getFood(food)
    except SearchError as er:
        raise(er)
    else:
        for i in target.ingredientsMenu.keys():
            info[i] = target.ingredientsMenu[i]
        for a in target.addOn.keys():
            info[a] = target.addOnMenu[a]
        
        info[food] = target.price
        print(f"food is {food}")
        if not info:
            raise SearchError('food')  
        return info


# take in a Drinks or Sides instance and extract information
# info = {[size]: f'{volumn}{unit} {price}'
def formatDS(food):
    info = {}
    for menu in [system.drinksMenu, system.sidesMenu]:
        for item in menu:
            if item.name == food:
                info[item.size] = f'{item.volumn}{item.unit} {item.price}'
    if not info:
        raise SearchError(f'{food}')
    return info

def computePrice(cart):
    price = 0
    try:
        info = formatDS(cart.name)
        print(f"DS info: {info}")
        for size in cart.items.keys():
            price += (int(info[size].split()[1]) * cart.items[size])
            
    except SearchError:
        try:
            info = formatMains(cart.name)
            print(f"Mains info: {info}")
            # print(cart.items)
            for item in cart.items.keys():
                price += (info[item] * cart.items[item])
            price += info[cart.name]
        except Exception as er:
            raise SearchError(f'{er} in conpute main price')
        
    # print(price)
    return price

def fetch_session_cart(id, food_name):
    # Creates a new cart first if the cart never existed
    id = int(id)
    if 'cart' not in session:
        print('cart not in session')
        cart = Cart(id,food_name)
        session['cart'] = cart.id
        orders[cart.id] = cart
    else:
        # Check the current cookie is valid
        print(f'cart {id} in session')
        try:
            target = orders[session['cart']]
            target.name = food_name
            return target
        except KeyError: 
            print('exception raised: cart not in session')
            cart = Cart(id, food_name)
            session['cart'] = cart.id
            orders[cart.id] = cart
            print("session cookie from ex: " ,session['cart'])
    return orders[session['cart']]

# a handler of root URL
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        
        if 'action' in request.form:
            # if user click "Check Status" button, ask for order ID
            if request.form['action'] == 'Check Status':
                return render_template('home.html', checkStatus=True)
            
            # if user click "Continue Order button, ask for order ID
            elif request.form['action'] == 'Continue my order':
                return render_template('home.html', continueOrder=True)
            
            # if user click "Make New Order" button, create new order and redirect to menu page
            elif request.form['action'] == 'Make New Order':
                order = system.makeOrder()
                # fetch_session_cart(order.orderId)
                return redirect(url_for('menu', id=order.orderId))
        
        elif 'furtherAction' in request.form:
            id = request.form['id']
            # if user insert orderID and comfirm "Check Status"
            if request.form['furtherAction'] == 'Check My Order!':
                # try to get the order, if Error can be catch, display error msg on the same page
                try:
                    order = system.getNextOrder(None, id)
                except (SearchError, ValueError) as er:
                    return render_template('home.html', form=request.form, checkStatus=True,error=str(er))
                
                # if no error occur, redirect to order detail page
                else:
                    return redirect(url_for('order_details', id=id, todo='checkStatus'))
                
            # if user insert orderID and confirm "Check Order"
            elif request.form['furtherAction'] == 'Continue My Order!':
                # try to get the order, if Error can be catch, display error msg on the same page
                try:
                    order = system.getNextOrder(None, id)
                except (SearchError, ValueError) as er:
                    return render_template('home.html', form=request.form, continueOrder=True, error=str(er))
                
                # if no error occur and the order is not submitted, redirect to order detail page
                else:
                    if order.orderStatus != 'Not Submitted':
                        er = "Your order has been submitted, please go to 'Check Status'"
                        return render_template('home.html',  form=request.form, continueOrder=True, error=er)
                    else:
                        return redirect(url_for('order_details', id=id, todo='continueOrder'))
            
    return render_template('home.html')

# displaying menu and handle ordering
@app.route("/menu/<id>", methods=["GET", "POST"])
def menu(id):
    try:
        order = system.getNextOrder(None,id)
    except SearchError as er:
        return render_template('errors.html', msg=str(er))

    nameList = []
    sizeList = []
    error = ''
    for i in order.orderedItem.keys():
        try:
            sizeList.append(i.size)
        except:
            sizeList.append(None)
        finally:
            nameList.append(i.name)
    # print(nameList)
    # print(sizeList)
    if request.method == "POST":
        
        if 'delete' in request.form:
            target = request.form['delete'].split()[1]
            size = sizeList[nameList.index(target)]
            print(target, size)
            try:
                food_to_delete = order.getFood(target,size)
            except SearchError as er:
                raise(er)
            print(food_to_delete)
            order.deleteFood(food_to_delete)
            
        elif 'confirm' in request.form:
            if len(order.orderedItem) == 0:
                error = 'Please order at least 1 item.'
                return render_template('menu.html', id=id, order=order, mainsM=system.mainsMenu, drinksM=system.drinksMenu, sidesM=system.sidesMenu,error=error)
            else:
                try:
                    system.confirmOrder(order)
                except StockError as er:
                    error = str(er)
                else:
                    print(system.stock)
                    return redirect(url_for('order_details', id=id, todo='checkStatus'))
    
    # print(orderDetail)
    return render_template('menu.html',id=id, order=order, mainsM=system.mainsMenu, drinksM=system.drinksMenu, sidesM=system.sidesMenu, error=error)


@app.route("/menu/<id>/Mains/<mains>", methods=["GET","POST"])
def Mains(id,mains):
    assert(mains!= None) # not necessary
    
    try:
        order = system.getNextOrder(None, id)
        food = system.getFood(mains)
    except SearchError as er:
        return render_template('errors.html', msg=str(er))
    
    # print('food is', food, 'type is ', type(food))
    cart = fetch_session_cart(id, mains)
    error = ""
    if request.method == 'POST':
        if 'add' in request.form:
            target = request.form['add'][7:]
            # print(target)
            try:
                num = int(request.form[f'quantity{target}'])
            except:
                error = "Please insert integer"
            else:
                if target == 'Ingredients':
                    target = request.form['Ingredients']
                    
                if num == 0:
                    cart.deleteFood(target)
                else:
                    cart.addFood(target,num, OVER_WRITE)
            
        elif 'confirm' in request.form:
            new_food = copy.deepcopy(food)
            if (mains == 'Burger') and ('Buns' not in cart.items.keys()):
                error = "Please order at least 1 buns."
            else:
                # print(order)
                for elem in new_food.ingredientsMenu.keys():
                    if elem in cart.items:
                        new_food.changeIngredients(elem, cart.items[elem])

                # print('after confirm', numBun)
                for elem in new_food.addOn:
                    if elem in cart._items:
                        new_food.addOn[elem] = cart._items[elem]

                order.addFood(new_food, 1)
                cart.empty()
                # print(new_food)
                price = computePrice(cart)
                return render_template('mains.html', food=new_food, price=price, finish=True, error=error)

        elif 'cancel' in request.form:
            cart.empty()
            return redirect(url_for('menu', id=id))
        
        elif 'return' in request.form:
            return redirect(url_for('menu', id=id))

    price = computePrice(cart)
    # print(f"errors is: {error}")
    return render_template('mains.html', food=food, orderedItem=cart.items, price=price, error=error)


@app.route("/menu/<id>/DrinksOrSides/<drinks_or_sides>", methods=["GET", "POST"])
def DrinksOrSides(id, drinks_or_sides):
    
    #print(info)
    error = ""
    cart = fetch_session_cart(id, drinks_or_sides)
    info = formatDS(drinks_or_sides)
    
    try:
        order = system.getNextOrder(None, id)
    except (SearchError, ValueError) as er:
        return render_template('errors.html',msg=str(er))
    if request.method == 'POST':
        if 'action' in request.form:
            if request.form['action'] == 'Delete All':
                cart.deleteFood(request.form['size'])
            elif request.form['quantity'] != '':
                try:
                    quantity = int(request.form['quantity'])
                except ValueError as er:
                    error = "Please insert integer."
                else:
                    if request.form['action'] == 'Add':
                        cart.addFood(request.form['size'],quantity)
                    elif request.form['action'] == 'Delete':
                        cart.deleteFood(request.form['size'], quantity)
            else:
                error='Please insert quantity with integer.'

        elif 'cancel' in request.form:
            cart.empty()
            return redirect(url_for('menu', id=id))
        
        elif 'confirm' in request.form:
            for size in cart.items.keys():
                food = system.getFood(drinks_or_sides, size)
                new_food = copy.deepcopy(food)
                order.addFood(new_food, cart.items[size])
            
            cart.empty()
            price = computePrice(cart)
            return render_template('drinks_or_sides.html', food=drinks_or_sides, info=info, price=price, error=error, orderedItem=cart._items, finish=True)
                
        elif 'return' in request.form:
            return redirect(url_for('menu', id=id))
    price = computePrice(cart)
    return render_template('drinks_or_sides.html', food=drinks_or_sides, info=info, price=price, error=error,orderedItem=cart._items)



# displaying order detail. If order is submitted, it allows user to refresh to get latest order status and optionally send email.
# If order is not submitted, it allows user to continue order by redirecting to menu page.
@app.route('/order/details/<todo>/<id>', methods=['GET', 'POST'])
def order_details(id, todo):
    id = int(id)
    try:
        order = system.getNextOrder(None, id)
    except (SearchError, ValueError) as er:
        return render_template('errors.html', msg=str(er))
    
    # order.updateOrder('Pending')
    msg = str(order)
    msg = Markup(msg.replace('\n', '<br/>'))
    status=order.orderStatus
    
    if request.method == 'POST':
        # if user would like to refresh order status
        if 'refresh' in request.form:
            status=order.orderStatus
            return render_template('order_details.html', msg=msg, status=status)
        
        # if user would like to send receipt to eamil
        elif 'sendEmail' in request.form and 'email' in request.form and request.form['email'] != "":
            return render_template('order_details.html', msg=msg, status=status, email=request.form['email'], send=True)
        
        # if the order is not submitted, and user want to continue ordering
        elif 'continueOrder' in request.form:
            return redirect(url_for('menu', id=id))
        
        elif 'pickup' in request.form:
            order.updateOrder("Picked Up")
            status=order.orderStatus
            return render_template('order_details.html', msg=msg, status=status)
    
    
    return render_template('order_details.html', msg=msg, status=status, todo=todo)

#beside each order has a button to indicate preparing/ready for pickup
@app.route('/staff',methods = ['GET', 'POST'])
def staff():
    msgList = [None]
    # msg = ''
    error = ''
    orderList = system.order


    if request.method == "POST":

        if 'prepare' in request.form:
            id = request.form['prepare'].split()[2]
            try:
                id = int(id)
            except:
                error = 'no such order'
            else:
                try:
                    order = system.getNextOrder(None,id)
                except SearchError as er:
                    error = str(er)
                else:
                    order.updateOrder('Preparing')
        
        elif 'ready' in request.form:
            id = request.form['ready'].split()[1]
            try:
                id = int(id)
            except:
                error = 'no such order'
            else:
                try:
                    order = system.getNextOrder(None,id)
                except SearchError as er:
                    error = str(er)
                else:
                    order.updateOrder('Ready')

        
    for elem in orderList:
        msg = str(elem)
        msg = Markup(msg.replace('\n', '<br/>'))
        msgList.append(msg)

    return render_template('staff.html', msgList = msgList,error = error)
    
@app.route('/stock',methods = ['GET', 'POST'])
def stock():
    
    stock = system.stock
    wholeStock = stock.whole
    error = ""
    print(wholeStock)
    if request.method == 'POST':
        
        if 'refill' in request.form:
            
            quantity = request.form['quantity']
            food = request.form['target']
            print(food)
            print(quantity)
            
            if quantity == '':
                # print('ggggggggggggggggggggggggggg')
                quantity = 0
            
            try:
                quantity = int(quantity)
            except Exception as er:
                error = str(er)
            else:
                # print(mainsQty)
                stock.increaseQuantity(food,quantity)
                print(stock)

    return render_template('stock.html', wholeStock = wholeStock,error=error)






# to run the project
if __name__ == "__main__":  # optionally add a name guard
    app.run(debug=True)
