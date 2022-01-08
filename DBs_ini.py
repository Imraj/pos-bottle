import time
#import date
import sqlite3

conn1 = sqlite3.connect('Items.db')
conn1.row_factory = lambda cursor, row: row[0]
conn2 = sqlite3.connect('ItemTranscitions.db')  #Sold items one by one,
conn3 = sqlite3.connect('Invoices.db')
conn1.execute('''CREATE TABLE Items
 
        (idcode INT PRIMARY KEY     NOT NULL,
  
 
         NAME           TEXT    NOT NULL,
         Category TEXT,
   
         Price        REAL NOT NULL,
         Qty INT NOT NULL);''')
#print ("Table items created successfully")
conn2.execute('''CREATE TABLE ItemsTranscitions 
 
 
       (TransID INT NOT NULL,
  
  
        Trans_date_time     Real    NOT NULL,
       Trans_item_idcode INT NOT NULL,
         Trans_selling_price Real not null,
         Trans_item_qty INT Not null);''')
#print ("Table Trans created successfully")
conn3.execute('''CREATE TABLE Invoices
 
        (InvoiceID INT PRIMARY KEY     NOT NULL, 
  
         Inv_date_time     Real    NOT NULL,
         Inv_items_idcodes INT NOT NULL,
         Inv_items_selling_price Real not null,
         Inv_items_qty INT Not null,
         Inv_totall_price Real Not null, 
         Inv_TAX Real Not Null, 

         Inv_Costumer_PNO INT NOT NULL,
         Inv_Payment_Method TEXT NOT NULL,
         Inv_Payment_ID INT,
         Inv_doneby TEXT NOT NULL );''')
print ("Table Invoices created successfully")
