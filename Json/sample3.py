import sqlite3

DB_PATH = 'product4.db'

def get_all_availableitems():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from productdetails')
        rows = c.fetchall()
        return { "count": len(rows), "product_id": rows }
    except Exception as e:
        print('Error: ', e)
        return None


def add_to_list(product_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("insert into userpurchase(product_id,product_name,product_price,product_details) select product_id,product_name,product_price,product_details from productdetails where product_id = '%s'" % product_id)
        c.execute('update userpurchase set product_quantity=1,purchase_price=product_price where product_id=?', (product_id))
        conn.commit()
        return {'product_id': product_id}
    except Exception as e:
        print('Error: ', e)
        return None

def get_all_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from userpurchase')
        rows = c.fetchall()
        return { "count": len(rows), "product_id": rows }
    except Exception as e:
        print('Error: ', e)
        return None

def get_item(product_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from userpurchase where product_id='%s'" % product_id)
        status = c.fetchone()[0]
        print(status)
        return status
    except Exception as e:
        print('Error: ', e)
        return None
    
def update_status(product_id,product_quantity):    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update userpurchase set product_quantity=? where product_id=?', (product_quantity,product_id))
        c.execute('update userpurchase set purchase_price=product_quantity*product_price')
        conn.commit()
        return {'product_id': product_id,'product_quantity':product_quantity}
    except Exception as e:
        print('Error: ', e)
        return None

def update_solditem(product_id,product_soldquantity,product_sellprice):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if int(product_soldquantity) > 0:
            c.execute('update userpurchase set product_soldquantity=? where product_id=?', (product_soldquantity,product_id))
            c.execute('update userpurchase set product_quantity=product_quantity-product_soldquantity where product_id=?', (product_id))
            c.execute('update userpurchase set product_sellprice=? where product_id=?', (product_sellprice,product_id))
            c.execute('update userpurchase set soldprice=product_soldquantity*product_sellprice where product_id=?', (product_id))
            conn.commit()
            return {'product_id': product_id}
        else:
            print("Specify postive value")
    except Exception as e:
        print('Error: ', e)
        return None


def delete_item(product_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('delete from userpurchase where product_id=?', (product_id))
        conn.commit()
        return {'product_id': product_id}
    except Exception as e:
        print('Error: ', e)
        return None
