# import Flask library
from flask import Flask, render_template, request, redirect, url_for, abort, Markup,session, make_response
from init import bootstrap_system#, ser, orders
from src.errors import StockError, SearchError, bun_error, check_numBuns_error, checkStock
from src.shoppingCart import Cart
import copy

# create a flask project, assigning to a variable called app
app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy

system = bootstrap_system()
# Loads data
orders = {}

# take in a Mains instance and extract information
def formatMains(food):
    assert(isinstance(food, Mains))

    pass


# take in a Drinks or Sides instance and extract information
def formatDS(food):
    info = {}
    for m in [system.drinksMenu, system.sidesMenu]:
        for i in m:
            if i.name == food:
                info[i.size] = f'{i.volumn}{i.unit} {i.price}'
                
    return info

def fetch_session_cart(id):
    # Creates a new cart first if the cart never existed
    id = int(id)
    if 'cart' not in session:
        print('cart not in session')
        cart = Cart(id)
        session['cart'] = cart.id
        orders[cart.id] = cart
    else:
        # Check the current cookie is valid
        print(f'cart {id} in session')
        try:
            return orders[session['cart']]
        except KeyError: 
            print('exception raised: cart not in session')
            cart = Cart(id)
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
                    return render_template('home.html',  form=request.form, checkStatus=True, error=er)
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

    else:
        orderDetail = str(order).replace('\n', '<br/>')
        # print(orderDetail)
        return render_template('menu.html',id=id, order=Markup(orderDetail), mainsM=system.mainsMenu, drinksM=system.drinksMenu, sidesM=system.sidesMenu)


@app.route("/menu/<id>/Mains/<mains>", methods=["GET","POST"])
def Mains(id,mains):
    assert(mains!= None) # not necessary
    '''
    if not request.cookies.get('mains'):
        res = make_response("Setting a cookie")
        info = {'numBun':0, 'numPat': 0, 'value': 0}
        ingredients = {}
        cookie = [info, ingredients]
        res.set_cookie('mains', cookie, max_age=60*60*24)
    else: 
        response = ""
        for c in cookie:
            for detail in c.keys():
                response += f"{detail}: {c[detail]}\n"
        res = make_response(response)
    return res
    '''
    # if 'post':
    #     modifyOrder(mains):
    #         try:
    #             item=system.getFood(mains)
    #         except:
            
    #         else:
    #             if 'confirm':
    #                 new_item = copy.deepcopy(item)
    #                 for a in new_item.addOn:
    #                     new_item.numBuns = request.form[a]

    try:
        food = system.getFood(mains)
    except SearchError as er:
        return render_template('errors.html', msg=str(er))
    # print('food is', food, 'type is ', type(food))

    cart = fetch_session_cart(id)
    try:
        order = system.getNextOrder(None, id)
    except (SearchError, ValueError) as er:
        return render_template('errors.html',error=str(er))
    if request.method == 'POST':
        numBun = 0
        numPat = 0
        cart = fetch_session_cart(id)
        if 'add' in request.form:
            target = request.form['add'][4:]
            # print(type(target)
            
            if request.form[target] == '':
                num = 0
            else:
                num = int(request.form[target])
            
            # print(cart._items)
            if target == 'Buns':
                numBun = num
                cart.addFood(target,num, True)
                print('numBun is ', numBun)
            elif target == 'Patties':

                numPat = num
                cart.addFood(target,num)
                print('numPat is ', numPat)
        
        ingreds = request.form['ingredients']
        # print('ingred is :', ingreds)
        ingredQty = request.form['quantity']
        
        # if (ingreds == ''):
        #     ingreds = None
        

        if (ingredQty == ''):
            ingredQty = 0

        if ingredQty != 0:
            cart.addFood(ingreds, int(ingredQty))
            # print(cart._items)
            # print('ingredqty is :', ingredQty)
        
        # print('food is', food)

        if 'confirm' in request.form:
            new_food = copy.deepcopy(food)
            try:
                # put food into ordered list
                order = system.getNextOrder(None,id)
                # ERROR order not found here
            except SearchError as er:
                return render_template('errors.html', msg=str(er))
            # print(order)
            
            
            # print(order)
            if ingredQty != 0:
                new_food.changeIngredients(ingreds,cart.items[ingreds])
            # print('after confirm', numBun)
            for elem in new_food.addOn:
                if elem in cart._items.keys():
                    num = cart._items[elem]
                    if elem == 'Buns':
                        new_food.addBuns(num)
                    elif elem == 'Patties':
                        new_food.addPats(num)
            # numBun = cart._items['Buns']
            # numPat = cart._items['Patties']
            # if (numBun != 0):
            #     new_food.addBuns(numBun)
            # if numPat != 0:
            #     new_food.addPats(numPat)
            print(new_food)
            order.addFood(new_food, 1)
            print(order)
            cart.empty()
            return render_template('mains.html', food=new_food,orderedItem=cart._items, finish=True)

        if 'cancel' in request.form:
            cart.empty()
            return redirect(url_for('menu', id=id))
        
        elif 'return' in request.form:
            return redirect(url_for('menu', id=id))

    return render_template('mains.html', food=food, orderedItem=cart._items)


@app.route("/menu/<id>/DrinksOrSides/<drinks_or_sides>", methods=["GET", "POST"])
def DrinksOrSides(id, drinks_or_sides):
    
    #print(info)
    error = ""
    info = formatDS(drinks_or_sides)
    cart = fetch_session_cart(id)
    try:
        order = system.getNextOrder(None, id)
    except (SearchError, ValueError) as er:
        return render_template('errors.html',error=str(er))
    if request.method == 'POST':
        cart = fetch_session_cart(id)
        if 'action' in request.form:
            if request.form['action'] == 'Delete All':
                cart.deleteFood(request.form['size'])
            elif request.form['quantity'] != '':
                try:
                    quantity = int(request.form['quantity'])
                except ValueError as er:
                    error = str(er)
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
            return render_template('drinks_or_sides.html', food=drinks_or_sides, info=info, error=error, orderedItem=cart._items, finish=True)
                
        elif 'return' in request.form:
            return redirect(url_for('menu', id=id))
        
    return render_template('drinks_or_sides.html', food=drinks_or_sides, info=info,error=error,orderedItem=cart._items)



# displaying order detail. If order is submitted, it allows user to refresh to get latest order status and optionally send email.
# If order is not submitted, it allows user to continue order by redirecting to menu page.
@app.route('/order/details/<todo>/<id>', methods=['GET', 'POST'])
def order_details(id, todo):
    id = int(id)
    try:
        order = system.getNextOrder(None, id)
    except (SearchError, ValueError) as er:
        return render_template('errors.html', msg=str(er))
    '''
    try:
        order.updateOrder('dfdf')
    except Exception as er:
        return render_template('errors.html', msg=str(er))
    '''
    # order.updateOrder('Pending')
    msg = str(order)
    msg = Markup(msg.replace('\n', '<br/>'))
    status=order.orderStatus
    
    if request.method == 'POST':
        # if user would like to refresh order status
        if 'refresh' in request.form:
            return render_template('order_details.html', msg=msg, status=status)
        
        # if user would like to send receipt to eamil
        elif 'sendEmail' in request.form and 'email' in request.form and request.form['email'] != "":
            return render_template('order_details.html', msg=msg, status=status, email=request.form['email'], send=True)
        
        # if the order is not submitted, and user want to continue ordering
        elif 'continueOrder' in request.form:
            return redirect(url_for('menu', id=id))
     
    
    return render_template('order_details.html', msg=msg, status=status, todo=todo)



# to run the project
if __name__ == "__main__":  # optionally add a name guard
    app.run(debug=True)
