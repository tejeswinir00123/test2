from flask import Flask
from flask_restful import Resource,Api,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///product4.db'
db=SQLAlchemy(app)

class Productdetails(db.Model):
    product_id=db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.String(200))
    product_price=db.Column(db.Integer())
    product_details=db.Column(db.String(500))

class userpurchase(db.Model):
    product_id=db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.String(200))
    product_price=db.Column(db.Integer())
    product_details=db.Column(db.String(500))
    product_quantity=db.Column(db.Integer())
    purchase_price=db.Column(db.Integer())
    product_soldquantity=db.Column(db.Integer())
    product_sellprice=db.Column(db.Integer())
    soldprice=db.Column(db.Integer())


#db.create_all()

cart_post_args=reqparse.RequestParser()
cart_post_args.add_argument("product_name",type=str,help="Product name is required",required=True)
cart_post_args.add_argument("product_price",type=str,help="Product price is required",required=True)
cart_post_args.add_argument("product_details",type=str,help="Product detail is required",required=True)

cart_update_args=reqparse.RequestParser()
cart_update_args.add_argument("product_name",type=str)
cart_update_args.add_argument("product_price",type=str)
cart_update_args.add_argument("product_details",type=str)

resource_fields = {
    'product_id':fields.Integer,
    'product_name':fields.String,
    'product_price':fields.Integer,
    'product_details':fields.String,
    }

class cartdetails(Resource):
    def get(self):
        product_names=Productdetails.query.all()
        carts={}
        for product_name in product_names:
            carts[product_name.product_id]={"product_name":product_name.product_name,"product_price":product_name.product_price,"product_details":product_name.product_details}
        return carts    
    
    
class cart(Resource):
    @marshal_with(resource_fields)
    def get(self,product_id):
        product_name=Productdetails.query.filter_by(product_id=product_id).first()
        if not product_name:
            abort(404,message="Could not find product with that id")
        return product_name
        
    @marshal_with(resource_fields)
    def post(self,product_id):
        args=cart_post_args.parse_args()
        product_name=Productdetails.query.filter_by(product_id=product_id).first()
        if product_name:
            abort(409,message="Product Id is already present")
        cart3=Productdetails(product_id=product_id,product_name=args['product_name'],product_price=args['product_price'],product_details=args['product_details'])
        db.session.add(cart3)
        db.session.commit()
        return cart3,201
    
    @marshal_with(resource_fields)
    def put(self,product_id):
        args=cart_update_args.parse_args()
        product_name=Productdetails.query.filter_by(product_id=product_id).first()
        if not product_name:
            abort(404,message="There is no product with this name")
        if args['product_name']:
            product_name.product_name=args['product_name']
        if args['product_price']:
            product_name.product_price=args['product_price']
        if args['product_details']:
            product_name.product_details=args['product_details']
        db.session.commit()
        return product_name
    
    @marshal_with(resource_fields)
    def delete(self,product_id):
        product_name=Productdetails.query.filter_by(product_id=product_id).first()
        if not product_name:
            abort(404,message="There is no product with this id")
        db.session.delete(product_name)
        db.session.commit()
        return 'Product Deleted',204
        

api.add_resource(cart,'/carts/<int:product_id>')
api.add_resource(cartdetails,'/carts')

if __name__=='__main__':
    app.run(debug=False)

