from flask import *  
import sqlite3  
  
app = Flask(__name__)  
 
@app.route("/")  
def index():
    conn = sqlite3.connect("product4.db")
    conn.row_factory = sqlite3.Row  
    c = conn.cursor()
    c.execute('select * from productdetails')
    rows = c.fetchall()
    return render_template("index.html",rows=rows)
     
 
@app.route("/add")  
def add():  
    return render_template("add.html")  
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            product_id = request.form["product_id"]    
            with sqlite3.connect("product4.db") as con:  
                cur = con.cursor()  
                cur.execute("insert into userpurchase(product_id,product_name,product_price,product_details) select product_id,product_name,product_price,product_details from productdetails where product_id = ?" , product_id)
                cur.execute("update userpurchase set product_quantity=1,purchase_price=product_price where product_id='%s'" % product_id)
                con.commit()  
                msg = "Product successfully purchased"  
        except:  
            con.rollback()  
            msg = "Product already purchased"  
        finally:  
            return render_template("success1.html",msg = msg)  
            con.close()  
 
@app.route("/view")  
def view():  
    con = sqlite3.connect("product4.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from userpurchase")  
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows)  

@app.route("/view1")  
def view1():  
    con = sqlite3.connect("product4.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from userpurchase")  
    rows = cur.fetchall()  
    return render_template("updatesuccess.html",rows = rows)

@app.route("/view2")  
def view2():  
    con = sqlite3.connect("product4.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from userpurchase")  
    rows = cur.fetchall()  
    return render_template("soldproduct.html",rows = rows)

@app.route('/update',methods=["POST"])
def update_status():
    if request.method=="POST":
        try:
            product_id=request.form["product_id"]
            product_quantity=request.form["product_quantity"]
            con = sqlite3.connect("product4.db")
            c = con.cursor()
            c.execute('update userpurchase set product_quantity=? where product_id=?', (product_quantity,product_id))
            c.execute('update userpurchase set purchase_price=product_quantity*product_price')
            con.commit()
            msg="Product quantity successfully updated"
        except Exception as e:
            con.rollback()
            return None
        finally:
            return render_template("view1.html")  
            con.close()  
 

@app.route('/updatesell',methods=["POST"])
def update_status1():
    if request.method=="POST":
        try:
            product_id=request.form["product_id"]
            product_soldquantity=request.form["product_soldquantity"]
            product_sellprice=request.form["product_sellprice"]
            con = sqlite3.connect("product4.db")
            c = con.cursor()
            c.execute('update userpurchase set product_soldquantity=? where product_id=?', (product_soldquantity,product_id))
            c.execute('update userpurchase set product_quantity=product_quantity-product_soldquantity where product_id=?', (product_id,))
            c.execute('update userpurchase set product_sellprice=? where product_id=?', (product_sellprice,product_id))
            c.execute('update userpurchase set soldprice=product_soldquantity*product_sellprice where product_id=?', (product_id,))
            con.commit()
            return render_template("view2.html")
        except Exception as e:
            print('Error: ', e)
            return None

@app.route("/delete")  
def delete():  
    return render_template("delete.html")  
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():
    if request.method=="POST":
        try:
            product_id = request.form["product_id"]
            con=sqlite3.connect("product4.db")  
            c = con.cursor()  
            c.execute("delete from userpurchase where product_id = ?",product_id)
            con.commit()
            msg = "Product successfully deleted"
            return render_template("delete_record.html",msg = msg)
        except:
            msg = "Product not present"  
        finally:  
            return render_template("delete_record.html",msg = msg)
            con.close()
  
if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5006, debug = True)
