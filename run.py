from sqlite3.dbapi2 import connect
from bottle import Bottle, template, route, run, response, static_file, request, get, post, redirect
from bottle import jinja2_template as template
import POS
import os
import random
import datetime
import time
# Import Bottle Extensions

import sqlite3 
import pandas as pd

app = Bottle()

ITEMS_DB = 'items.db'
INVOICES_DB = 'invoices.db'
TRANS_DB = 'itemTranscitions.db'


@route("/")
def home():
    #return "Home"
    items_count = POS.get_items_count()
    transaction_count = POS.get_transaction_count()
    invoices_count = POS.get_invoices_count()
    return template('index', items_count=items_count, transaction_count=transaction_count, invoices_count=invoices_count)

@get("/new_item")
def new_item():
    return template('new_item')

@route('/upload_item', method='POST')
def do_upload():
    upload = request.files.get('itemsfile') #request.POST['itemfile']
    name, ext = os.path.splitext(upload.filename)
    #print("Name: {}, Ext: {}".format(name, ext))
    #print("{}".format(upload.file))
    if ext not in ('.xlsx', '.csv', '.db'):
        #return "File extension not allowed."
        return template('new_item', res="error")

    if ext == ".csv":
        fname = name + '.csv'
        df = pd.read_csv(upload.file)
        print("DataFrame: {}".format(df))
        for index,item in df.iterrows():
            item_code =item['Id']
            name = item['Name']
            category = item['Category']
            price = item['Price']
            quantity = item['Quantity']
            if name != None or category != None or price != None or quantity != None:
                POS.add_item(item_idcode=item_code, item_name=name, item_category=category, item_price=price, quantity=quantity)
        return template('new_item', res="success")
       

    if ext == ".xlsx":
        df = pd.read_excel(upload.file)
        for index,item in df.iterrows():
            item_code = item['Id']
            name = item['Name']
            category = item['Category']
            price = item['Price']
            quantity = item['Quantity']
            if name != None or category != None or price != None or quantity != None:
                POS.add_item(item_idcode=item_code, item_name=name, item_category=category, item_price=price, quantity=quantity)
        return template('new_item', res="success")

    if ext == ".db":
        try:
            conn = sqlite3.connect(upload.file)    
        except Exception as e:
            print(e)
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Items")
        all_items = cursor.fetchall()
        for ait in all_items:
            item_code = ait['idcode']
            name = ait['Name']
            category = ait['Category']
            price = ait['Price']
            quantity = ait['Qty']
            if name != None or category != None or price != None or quantity != None:
                POS.add_item(item_idcode=item_code, item_name=name, item_category=category, item_price=price, quantity=quantity)
        return template('new_item', res="success")
           

@post("/new_item")
def new_item():
    item_code = request.forms.get('id')
    name = request.forms.get('name')
    category = request.forms.get('category')
    price = request.forms.get('price')
    quantity = request.forms.get('quantity')
    print("Name: {}, Qty: {}, code: {}".format(name, quantity, item_code))
    if name != None or category != None or price != None or quantity != None:
        POS.add_item(item_idcode=item_code, item_name=name, item_category=category, item_price=price, quantity=quantity)
        return template('new_item', res="success")

@get("/plogin/<username>/<password>")
def plogin(username,password):
    #username = request.forms.get("username")
    #password = request.forms.get("password")
    try:
        luser = POS.get_user(username, password)
        print("Luser: {}".format(luser))
        if luser == None:
             return {"res": "invalid"}
        else:
            return {"res": "sucess", "user":luser}
    except:
        return {"res": "error"}

@get("/login")
def login():
    return template("login")

@get("/register")
def register():
    return template("register")

@post("/pregister")
def pregister():
    username = request.forms.get("username")
    password = request.forms.get("password")
    name = request.forms.get("name")
    cashierId = request.forms.get("cashierId")
    
    POS.create_user(username, password, name, cashierId)
    print("U00: {}, {}, {}, {}".format(username, password, name, cashierId))

    redirect("/login")


@get("/delete_item_api/<id_code>")
def delete_item(id_code):
    items = POS.get_all_items()
    try:
        POS.delete_item(id_code)
        return {"res": "success"}
    except:
        return {"res": "error"}

@get('/api/update_item_name/<id_code>/<name>')
def update_item_name(id_code,name):
    try: 
        POS.update_name(id_code, name)
        return {"res": "success"}
    except: return {"res": "error"}

@get('/api/update_item_category/<id_code>/<category>')
def update_item_category(id_code, category):
    try: 
        POS.update_category(id_code,category)
        return {"res": "success"}
    except: return {"res": "error"}

@get("/api/update_item_quantity/<id_code>/<quantity>")
def update_item_quantity(id_code, quantity):
    try: 
        POS.update_quantity(id_code, quantity)
        return {"res": "success"}
    except: return {"res": "error"}

@get("/api/update_item_price/<id_code>/<price>")
def update_item_price(id_code, price):
    try: 
        POS.update_price(id_code, price)
        return {"res": "success"}
    except: return {"res": "error"}

@get("/api/save_transaction/<id_code>/<item_price>/<sold_item_qty>")
def save_transaction(id_code, item_price, sold_item_qty):
    min = 1111
    max = 999999999
    randomNum = random.randrange(min, max)
    Trans_ID = randomNum
    Creation_datetime = int(time.strftime("%Y%m%d%H%M")) #datetime.datetime.now()
    item_idcode = id_code
    item_price = item_price
    sold_item_qty = sold_item_qty
    try:
        print("Creation-DateTime:{}, Trans_ID: {}, id_code:{}, price: {}, qty:{}".format(Trans_ID, Creation_datetime,item_idcode,item_price,sold_item_qty))
        POS.TransictionSaver(Trans_ID,Creation_datetime,item_idcode,item_price,sold_item_qty)
        return {"res": "success"}
    except:
        return {"res": "error"}

@get("/transactions")
def get_transactions():
    try:
        trans = POS.get_all_transaction()
        #return {"res": "success", "Transactions": trans}
    except:
        trans = "None"
    return template("transactions", transactions=trans)

@get("/transactions_api")
def get_transactions():
    try:
        trans = POS.get_all_transaction()
        return {"res": "success", "transactions": trans}
    except:
         return {"res": "error"}


@get("/get_transaction_api/<id>")
def get_transaction(id):
    try:
        trans = POS.Get_Trans(id)
        return {"res": "success", "Transactions": trans}
    except:
        return {"res": "error"}

@get("/get_item_transaction_api/<id_code>")
def get_item_transaction(id_code):
    try:
        trans = POS.Get_Item_Trans(id_code)
        return {"res": "success", "transactions": trans}
    except:
        return {"res": "error"}

@get("/items")
def items():
    items = POS.get_all_items()
    return template("items", rows=items)


@get("/items_api")
def items():
    items = POS.get_all_items()
    itemsArr = []
    for item in items:
        #print("Codes: {:.20f}".format(item["idcode"]))
        itemsArr.append( (item["idcode"], item["Name"], item["Category"], item["Price"] ,item["Qty"]) )
    return {"items": itemsArr}

@route("/item/<id_code>")
def get_item(id_code):
    id = id_code
    item = POS.get_item_info(id)
    if item != None:
        return template('get_item', item=item)

@get("/item_api/<id_code>")
def get_item_api(id_code):
    item = POS.get_item_info(id_code)
    return {"Id": item["idcode"],"name": item["Name"], "Category": item["Category"], "Price": item["Price"], "Qty": item["Qty"]}

@route("/new_cart")
def new_cart():
    return template('new_cart')

@route("/new_invoice")
def create_invoice():
    return template('create_invoice')

@post("/save_invoice")
def save_invoice():
    #InvID,CashierID_Name,Costumer_PNO,Payment_ID,Payment_Method="CASH",StoreName="NULL"
    invId = request.forms.get("inventoryId")
    cashierId_Name = request.forms.get("cashier")
    customer_PNO = request.forms.get("customer")
    paymentId = request.forms.get('paymentId')
    paymentMethod = request.forms.get("paymentMethod")
    storeName = request.forms.get("store", "NULL")
    POS.Saveinvoice(invId, cashierId_Name, customer_PNO, paymentId, paymentMethod, storeName)

#params=(TransID,Invoice_datetime,Cart_items_idcodes,Cart_items_prices,Cart_items_Qty,totall_price,
# TAXs,Costumer_PNO,Payment_Method,Payment_ID,CashierID_Name)
@route('/<filename>.css')
def stylesheets(filename):
    return static_file('{}.css'.format(filename), root='static')

@get("/api/save_invoice/<invoiceId>/<cartItems>/<cartPrices>/<cartQty>/<totalPrice>/<Tax>/<dateTime>/<customerPNO>"+
"/<paymentMethod>/<paidAmount>/<paymentId>/<cashierIdName>")
def save_invoice(invoiceId,cartItems,cartPrices,cartQty,totalPrice,Tax,dateTime,customerPNO,paymentMethod,paidAmount,paymentId,cashierIdName):

    print("Inv: {},{}, {}, {}, {}, {}, {}, {}, {}, {}".format(
        invoiceId, cartItems, cartPrices, cartQty, totalPrice, Tax, dateTime, customerPNO,
        paymentMethod, paidAmount,paymentId,cashierIdName
    ))

    try:
        print("cartItems: {}={}".format(cartItems, cartPrices))
        POS.SaveInvoice(invoiceId, str(cartItems), str(cartPrices), str(cartQty), totalPrice, Tax, str(dateTime), 
        customerPNO, paymentMethod, paidAmount,paymentId,cashierIdName)
        return {"res": "success"}
    except:
        print("Error saving invoice.")
        return {"res": "error"}


@route("/invoices")
def invoices():
    return template('invoices')

@get("/api/invoices")
def invoices():
    try:
        invoices = POS.GetInvoices()
        return {"res": "success", "invoices": invoices}
    except:
        return {"res": "error"}

@route('/invoice/<inv_id>')
def invoice(inv_id):
    return template("invoice")

@get("/api/invoice/<invId>")
def invoices(invId):
    try:
        invoice = POS.GetInvoice(invId)
        print("New Invoice:{}".format(invoice))
        return {"res": "success", "invoice": invoice}
    except:
        return {"res": "error"}

#run(host='localhost', port='8080', debug=True, reloader=True)
print("OS Env: {} Port: {}".format(os.environ.get('DYNO'), os.environ.get("PORT")))
if os.environ.get('DYNO') != None:
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
elif os.environ.get('DYNO') == None:
    run(host='localhost', port=8080, debug=True)