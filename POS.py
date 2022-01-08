import csv
import pandas as pd
import pushdb
import time
#import pdf

def add_item(item_idcode,item_name,item_category,item_price,quantity):
	pushdb.AddItem(item_idcode,item_name,item_category,item_price,quantity)

def get_all_items():
	items = pushdb.GetItems()
	return items

def get_items_count():
	c = pushdb.GetItemsCount()
	print("CCount1: {}".format(c[0]))
	return int(c[0])

def get_transaction_count():
	c = pushdb.GetTransactionCount()
	return int(c[0])

def get_invoices_count():
	c = pushdb.GetInvoicesCount()
	return int(c[0])

def update_name(item_idcode,name):
	pushdb.UpdateName(item_idcode,name)

def update_price(item_idcode,item_price):
	pushdb.UpdatePrice(item_idcode,item_price)

def update_quantity(item_idcode,quantity):
	pushdb.UpdateQty(item_idcode,quantity)

def update_category(item_idcode,category):
	pushdb.UpdateCategory(item_idcode,category)

def delete_item(item_idcode):
	pushdb.DeleteItem(item_idcode)

def get_item_info(item_idcode):
	item_info = pushdb.GetItem(item_idcode) # Returns with Name, Quantity & Price.
	return (item_info)

def Get_Trans(TransID): #TransID = InvoiceID
	try:
		Trans=pushdb.GetTrans(TransID)
		return(Trans)
	except: return("No Transictions By this ID.")

def get_user(username, password):
	try:
		user = pushdb.GetUser(username,password)
		print("get_user::{}".format(user))
		return user
	except: return "This account doesn't exist"

def create_user(username, password, name, cashierId):
	try:
		print("Create User....")
		pushdb.CreateUser(username,password,name,cashierId)
		print("Create User....")
	except:
		print("No user creation")
		return "Couldn't create user"

def get_all_transaction():
	try:
		trans = pushdb.GetAllTransaction()
		return trans
	except:
		return "No Transaction"

def Get_Item_Trans(item_idcode):
	try:
		ItemTrans=pushdb.GetItemTrans(item_idcode)
		
		return(ItemTrans)
	except: return("No Transictions for this Item.")


def TransictionSaver(Trans_ID,Creation_datetime,item_idcode,item_price,sold_item_qty):
	pushdb.SaveTransiction(Trans_ID,Creation_datetime,item_idcode,item_price,sold_item_qty)


def Qty_check(item_idcode,Ordered_Qty):
	if get_item_info(item_idcode)[1]>0:
		if get_item_info(item_idcode)[1]<Ordered_Qty:
			return("Low Item Stock,{0}".format(get_item_info(item_idcode)[1]))
		else:
			return("OKAY")
	else: return("ZERO Stock")



def StartNewCart(item_scanned_idcode,item_Price,item_quantity=1):
	FirstItem=("idcode,Price,Qty\n{0},{1},{2}\n".format(item_scanned_idcode,item_Price,item_quantity))
	with open('cart.csv','r+') as Cart:
		Cart.truncate(0)
		Cart.write(FirstItem)

def AddtoCart(item_scanned_idcode,item_Price,item_quantity=1):
	toAdd=("{0},{1},{2}\n".format(item_scanned_idcode,item_Price,item_quantity))
	#print(toAdd)
	with open('cart.csv','a') as Cart:
		Cart.write(toAdd)
	#Cart.save()
def updateQtyCart(item_idcode,newQty):
	oldCart = pd.read_csv("cart.csv")
	oldCart.loc[oldCart["idcode"]==item_idcode, "Qty"] = newQty
	oldCart.to_csv("cart.csv", index=False)

def Delete_inCart_item(item_idcode):
	#try:
		oldCart = pd.read_csv("cart.csv")
		oldCart = oldCart.set_index("idcode",inplace=False)
		#data_with_index.head()
		#oldCart.loc[oldCart["idcode"]==item_idcode)
		print(item_idcode)
		newCart = oldCart.drop(item_idcode)
		newCart.to_csv("cart.csv", index=True)
		return(newCart)
		#print(newCart)
	#except: print(Exception)
def Calc(item_priceS,item_quantityS,Discount_onall=0,TAX=0.15):
	
	Actual_cost=[]
	counter=0
	Sum_exTAX=0

	Sum_inTAX=0

	for prices in item_priceS:
			prices=float(prices)
			Qty=int(item_quantityS[counter])
			ACost=prices*Qty
			Actual_cost.append(ACost)
			counter=counter+1
	#print(Actual_cost)
	for individual_cost in Actual_cost:
		Sum_exTAX=Sum_exTAX+individual_cost
	
	if Discount_onall>0:
		Discount=Sum_exTAX*Discount_onall
		if Discount < Sum_exTAX:
			Sum_exTAX=Sum_exTAX-Discount
		else: pass

	
	TAXs=Sum_exTAX*TAX
	Sum_inTAX=Sum_exTAX+TAXs
	#print(Sum_exTAX)
	#print(Sum_inTAX)
	return(Actual_cost,Sum_exTAX,TAXs,Sum_inTAX)
def Cart_ini():
	items_idcodes_inCart=[]
	items_priceS_inCart=[]
	items_QtyS_inCart=[]
	with open('cart.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				#print(f'Column names are {", ".join(row)}')
				line_count += 1
			else:
				idcode=row[0]
				items_idcodes_inCart.append(idcode)
				Price=row[1]
				items_priceS_inCart.append(Price)
				Quantity=row[2]
				items_QtyS_inCart.append(Quantity)
				#print(idcode,Price,Quantity)
				line_count += 1
	Calculate=Calc(items_priceS_inCart,items_QtyS_inCart)
	individual_costs=Calculate[0]
	Total_cost_ExTAX=Calculate[1]
	TAXs=Calculate[2]
	Total_cost_InTAX=Calculate[3]


	return(items_idcodes_inCart,individual_costs,Total_cost_ExTAX,TAXs,Total_cost_InTAX,items_QtyS_inCart)


#params=(TransID,Invoice_datetime,Cart_items_idcodes,Cart_items_prices,Cart_items_Qty,totall_price,
# TAXs,Costumer_PNO,Payment_Method,Payment_ID,CashierID_Name)

#Saveinvoice(invId, invoiceDateTime,cartItems, cartPrices, cartQty, totalPrice, tax, customerPNO,
#    paymentMethod,paymentId,cashierIdName)
def GetInvoices():
	invoices = pushdb.GetAllInvoice()
	return invoices

def SaveInvoice(invId, cartItems, cartPrices, cartQty, totalPrice, tax, dateTime, customerPNO,
   paymentMethod, paidAmount,paymentId,cashierIdName):

   pushdb.SaveInvoice(
	   	invId, cartItems, cartPrices, cartQty, totalPrice, tax, dateTime, customerPNO,
   		paymentMethod, paidAmount,paymentId,cashierIdName
	)

def Saveinvoice(InvID,CashierID_Name,Costumer_PNO,Payment_ID,Payment_Method="CASH",StoreName="NULL"):
	Invoice_datetime=int(time.strftime("%Y%m%d%H%M"))#yr,month,day,Hour,min.
	CartData=Cart_ini()
	Cart_items_idcodes=CartData[0]
	Cart_items_prices=CartData[1]
	Total_NoTAXs=CartData[2]
	TAXs=CartData[3]
	Cart_items_Qty=CartData[5]
	inv=pushdb.SaveInvoice(InvID,Invoice_datetime,Cart_items_idcodes,Cart_items_prices,Cart_items_Qty,Total_NoTAXs,TAXs,Payment_ID,Costumer_PNO,CashierID_Name,Payment_Method)
	return("DONE")

def GetInvoice(invID):
	invoice = pushdb.GetInvoice(invID)
	return invoice

def Recall_invoice(InvID):
	Full_Inv=pushdb.GetInvoice(InvID)
	Vars=["Invid","Inv_datetime","Items","Prices","Qty","Total_NoTAXs","TAXs","Payment_ID","Payment_Method","Costumer_PNO","Cashier"]	
	#Items=Inv[2]
	#Prices=Inv[3]
	#Qty=Inv[4]
	counter1=0
	for i in Full_Inv:
		

		if len(Full_Inv)==counter1:
			break
		else:

			Vars[counter1]=i
			print(Vars[counter1])
			counter1=counter1+1







	return(Full_Inv,Vars)
	#Invoice='''<!DOCTYPE html><html dir="rtl" lang="ar">'''
	#make_sure item Qs not ZERO
	
def invoice_maker(InvID):
	InvoiceData=Recall_invoice(InvID)[1]
	#Vars=["Invid","Inv_datetime","Items","Prices","Qty","Total_NoTAXs","TAXs","Payment_ID","Payment_Method","Costumer_PNO","Cashier"]
	Invoice='''<!DOCTYPE html><html dir="rtl" lang="ar">
	        <body style="width:360px ; height:660px;" >

		{0} / invid</br>
		{1} / Time</br>
		{2}/ items</br>
		i names / </br>
		i names / </br>

		{3} / prcs</br>
		{4}/ qty</br>
		{5} / tot-txs</br>
		{6}/taxs</br>
		tot+txs / </br>

		{7} /pyid </br>

		{8}/ mthd</br>
		{9} costidpno</br>
		{10} cshr</br>
		</br>

	<body></html>'''.format(InvoiceData[0],InvoiceData[2],InvoiceData[3],InvoiceData[4],InvoiceData[5],InvoiceData[6],InvoiceData[7],InvoiceData[8],InvoiceData[9],InvoiceData[10])
	#name=str(InvID)
	#pdf.pdf(a,name)

	#get_item_price_from_db
#print(Cart[0])  
#Calc(Cart[1],Cart[2])
#AddtoCart("667","0.9",0.5)
#with open('cart.csv') as Cart:
#		print(Cart.read())
#updateQty(667,1)
#Delete_inCart_item(667)
#with open('cart.csv') as Cart:
#		print(Cart.read())
