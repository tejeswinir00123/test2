from flask import *  
import sqlite3  
  
app = Flask(__name__)  
 
@app.route("/")  
def index():  
    return render_template("indexadmin.html");  
 
@app.route("/add")  
def add():  
    return render_template("addadmin.html")  
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            product_id = request.form["product_id"]  
            product_name = request.form["product_name"]  
            product_price = request.form["product_price"]
            product_details=request.form["product_details"]
            with sqlite3.connect("product4.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Productdetails (product_id,product_name,product_price,product_details) values (?,?,?,?)",(product_id,product_name,product_price,product_details))  
                con.commit()  
                msg = "Product details added scuccessfully"  
        except:  
            con.rollback()  
            msg = "Product cannot be added as the product id is already used"  
        finally:  
            return render_template("successadmin.html",msg = msg)  
            con.close()  
 
@app.route("/view")  
def view():  
    con = sqlite3.connect("product4.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Productdetails")  
    rows = cur.fetchall()  
    return render_template("viewadmin.html",rows = rows)  
 
@app.route("/view2")  
def view2():  
    con = sqlite3.connect("product4.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Productdetails")  
    rows = cur.fetchall()  
    return render_template("updateproductadmin.html",rows = rows)

@app.route("/updateadmin")  
def updateadmin():  
    return render_template("updateadmin.html")  
 
@app.route('/update',methods=["POST","GET"])
def update():
    if request.method=="POST":
        try:
            product_id=request.form["product_id"]
            product_price=request.form["product_price"]
            product_details=request.form["product_details"]
            con = sqlite3.connect("product4.db")
            c = con.cursor()
            c.execute('update Productdetails set product_price=?,product_details=? where product_id=?', (product_price,product_details,product_id))
            con.commit()
            msg="Product details successfully updated"
        except Exception as e:
            con.rollback()
            return None
        finally:
            return render_template("view2admin.html",msg=msg)  
            con.close()  
  
@app.route("/delete")  
def delete():  
    return render_template("deleteadmin.html")  
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    product_id = request.form["product_id"]  
    with sqlite3.connect("product4.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Productdetails where product_id = ?",product_id)  
            msg = "Product successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_recordadmin.html",msg = msg)  
  
if __name__ == "__main__":  
    app.run(debug = True)  
