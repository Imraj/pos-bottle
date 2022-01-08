import time
#import date
import sqlite3

#from run import invoices

conn1 = sqlite3.connect('Items.db')
conn1.row_factory = sqlite3.Row #lambda cursor, row: row[0]
conn2 = sqlite3.connect('ItemTranscitions.db')  #Sold items one by one,
conn3 = sqlite3.connect('Invoices.db')
conn4 = sqlite3.connect('Users.db')

cruItems = conn1.cursor()
cruitemtrans = conn2.cursor()
cruinv = conn3.cursor()
cruser = conn4.cursor()

###>>> ItemsDB: Routine Items & products DB, Based on Unique Item IDcode (Scanned Baracode).
def AddItem(idcode,item_name,item_category,item_price,item_Qty):
  conn1.execute("INSERT INTO Items (idcode,NAME,Category,Price,Qty) VALUES ({0}, '{1}','{2}',{3},{4})".format(idcode,item_name,item_category,item_price,item_Qty))
  conn1.commit()
  print ("Item created successfully")

def GetItems():
  cruItems.execute("SELECT * FROM Items")
  items = cruItems.fetchall()
  #cruItems.close()
  return items

def GetItemsCount():
  cruItems.execute('SELECT Count(*) FROM Items')
  count = cruItems.fetchone()
  return count

def GetTransactionCount():
  cruitemtrans.execute('SELECT Count(*) FROM ItemsTranscitions')
  count = cruitemtrans.fetchone()
  return count

def GetInvoicesCount():
  cruinv.execute('SELECT Count(*) FROM Invoices')
  count = cruinv.fetchone()
  return count

def GetUser(username, password):
  cruser.execute('''SELECT * FROM Users WHERE username=? AND password=?''',(username, password))
  user = cruser.fetchone()
  return user

def CreateUser(username, password, name, cashierId):
   conn4.execute(''' INSERT INTO Users VALUES(?,?,?,?)''',(name, username, cashierId, password))
   #conn4.execute("INSERT INTO Users (Name,Username,Password,cashierId) VALUES ('{0}','{1}','{2}','{3}')".format(name, username, cashierId, password ))
   conn4.commit()
   print ("User created successfully : {}, {}, {}".format(username, name, cashierId))


def GetItem(item_idcode):
  cruItems.execute(''' SELECT * FROM Items WHERE idcode=?''',(item_idcode,))
  item= cruItems.fetchone()
  return item

def GetAllIteminfo(item_idcode): 
#to get all info: name,category,price,qty,Transictions,Trans_qty,Totall_sales of item.
  pass

def DeleteItem(item_idcode):
  cruItems.execute(''' DELETE FROM Items WHERE idcode=?''',(item_idcode,))
  conn1.commit()

def UpdateName(item_idcode,Name):
  cruItems.execute(''' UPDATE Items SET Name=?  WHERE idcode=?''',(Name,item_idcode))
  conn1.commit()

def UpdateCategory(item_idcode,Category):
  cruItems.execute(''' UPDATE Items SET Category=?  WHERE idcode=?''',(Category,item_idcode))
  conn1.commit()

def UpdateQty(item_idcode,New_quantity):
  cruItems.execute(''' UPDATE Items SET Qty=?  WHERE idcode=?''',(New_quantity,item_idcode))
  conn1.commit()

def UpdatePrice(item_idcode,New_Price):
  cruItems.execute(''' UPDATE Items SET Price=?  WHERE idcode=?''',(New_Price,item_idcode))
  conn1.commit()


#InvoiceID = TransID
###>>> ItemsTransictions: Save Sold Items one by one, Spliting the Cart based on Items & store it, 
###....for Future Analysis.
def SaveTransiction(Trans_ID,Creation_datetime,item_idcode,item_price,sold_item_qty):
  conn2.execute(''' INSERT INTO ItemsTranscitions 
    (TransID,Trans_date_time,Trans_item_idcode,Trans_selling_price,Trans_item_qty) VALUES ({0},{1},{2},{3},{4})'''.format(Trans_ID,Creation_datetime,item_idcode,item_price,sold_item_qty));
  conn2.commit()
  return("DONE")

def GetTrans(TransID): #To Get a specific Transiction., InvoiceID or TransID are the Same.
  cruitemtrans.execute(''' SELECT * FROM ItemsTranscitions WHERE TransID=?''',(TransID,))
  Trans_data= cruitemtrans.fetchall()
  return(Trans_data)

def GetItemTrans(item_idcode): # Get a specific Item All Transictons.
  cruitemtrans.execute(''' SELECT * FROM ItemsTranscitions WHERE Trans_item_idcode=?''',(item_idcode,))
  Trans_data= cruitemtrans.fetchall()
  return(Trans_data)

def GetAllTransaction(): # Get All Transictons.
  cruitemtrans.execute(''' SELECT * FROM ItemsTranscitions ''')
  Trans_data= cruitemtrans.fetchall()
  return(Trans_data)


###>>> InvoicesDB: Save Sales, as whole Cart, store it based on InvoiceID or TransID, <InvoiceID = TransID>

###....for Daily routine sales.
###>>> We use InvoicesDB to generate printed & electronic Invoices. 
def SaveInvoice(TransID,Cart_items_idcodes,Cart_items_prices,Cart_items_Qty,totall_price,TAXs,dateTime,Costumer_PNO,Payment_Method,paidAmount,Payment_ID,CashierID_Name):
  #Cart_items_idcodes=[str(int) for int in Cart_items_idcodes]
  #Cart_items_idcodes=",".join(Cart_items_idcodes)
  #Cart_items_prices=[str(int) for int in Cart_items_prices]
  #Cart_items_prices=",".join(Cart_items_prices)
  #Cart_items_Qty=[str(int) for int in Cart_items_Qty]
  #Cart_items_Qty=",".join(Cart_items_Qty)
  print("SaveInvoice: {} {} {}".format(Cart_items_idcodes,Cart_items_prices,Cart_items_Qty))
  
  params=(TransID,Cart_items_idcodes,Cart_items_prices,Cart_items_Qty,totall_price,TAXs, dateTime,Costumer_PNO,Payment_Method, paidAmount,Payment_ID,CashierID_Name)
  conn3.execute('''INSERT INTO Invoices VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''',params)
  conn3.commit()
  
  return("Done")

def GetAllInvoice():
  cruinv.execute(''' SELECT * FROM Invoices ''')
  invoices = cruinv.fetchall()
  return invoices

def GetInvoice(InvoiceID):
  try:
    cruinv.execute(''' SELECT * FROM Invoices WHERE InvoiceID=?''',(InvoiceID,))
    invoice= cruinv.fetchone()
    return invoice
  except:
    return("NO Invoices with this InvID")

  Inv_items_idcodes = [int(str) for str in Inv_data[0][2].split(",")]
  Inv_items_prices = [float(str) for str in Inv_data[0][3].split(",")]
  try:
    Inv_items_Qty = [int(str) for str in Inv_data[0][4].split(",")]
  except:
    Inv_items_Qty =  Inv_data[0][4]


  return(Inv_data[0])


#########3333 DBs Structure#####
#conn1.execute('''CREATE TABLE Items
 
#        (idcode INT PRIMARY KEY     NOT NULL,
  
 
 #        NAME           TEXT    NOT NULL,
  #       Category TEXT,
   
   #      Price        REAL NOT NULL,
    #     Qty INT NOT NULL);''')
#print ("Table items created successfully")
#conn2.execute('''CREATE TABLE ItemsTranscitions 
 
 
    #   (TransID INT NOT NULL,
  
  
   #     Trans_date_time     Real    NOT NULL,
  #     Trans_item_idcode INT NOT NULL,
 #        Trans_selling_price Real not null,
#         Trans_item_qty INT Not null);''')
#print ("Table Trans created successfully")
#conn3.execute('DROP TABLE Invoices')
#conn3.execute('''CREATE TABLE Invoices
#         (InvoiceID INT PRIMARY KEY   NOT NULL, 
#          Inv_items_idcodes TEXT NOT NULL,
#          Inv_items_selling_price TEXT not null,
#          Inv_items_qty TEXT Not null,
#          Inv_totall_price Real Not null,
#          Inv_paid_amount Real NOT NULL,
#          Inv_TAX Real Not Null, 
#          Inv_dateTime VARCHAR NOT NULL,
#          Inv_Costumer_PNO INT NOT NULL,
#          Inv_Payment_Method TEXT NOT NULL,
 #         Inv_Payment_ID INT,
#          Inv_doneby TEXT NOT NULL );''')

#print ("Table Invoices created successfully")

#conn4.execute('DROP TABLE Users')
#conn4.execute('''CREATE TABLE Users
#                (Name  VARCHAR  NOT NULL,
#                 Username VARCHAR NOT NULL,
#                 casherId VARCHAR NOT NULL,
#                 Password VARCHAR NOT NULL
#              );''')
#print ("Table user created successfully")
