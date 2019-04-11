# import Flask library
from flask import Flask, render_template, request, redirect, url_for, abort, Markup

# create a flask project, assigning to a variable called app
app = Flask(__name__)

# a handler of root URL
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        if 'checkStatus' in request.form:
            return render_template('home.html', checkStatus=True)
        
        elif 'continueOrder' in request.form:
            return render_template('home.html', continueOrder=True)
        
        elif 'newOrder' in request.form:
            return redirect(url_for('menu'))
        
        elif 'confirmCS' in request.form:
            return redirect(url_for('order_details', id=reqeust.form['id']))
        
        elif 'confirmCO' in request.form:
            return redirect(url_for('menu', id=request.form['id']))
        
    return render_template('home.html')

# displaying menu and handle ordering
@app.route("/menu", methods=["GET", "POST"])
def menu(id=None):
    
    
    
    return render_template('menu.html')

# displaying confirmed order details (receipt), and provide 'send receipt' option
@app.route('/order/details', methods=['GET', 'POST'])
def order_details():
    

    return render_template('order_details.html')


# to run the project
if __name__ == "__main__":  # optionally add a name guard
    app.run(debug=True)
