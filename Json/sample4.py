import sample3
from flask import Flask, request, Response
import json

app = Flask(__name__)


@app.route('/items/allproducts')
def get_all_availableitems():
   res_data = sample3.get_all_availableitems()
   response = Response(json.dumps(res_data), mimetype='application/json')
   return response


@app.route('/item/new', methods = ['POST'])
def add_item():
   req_data=request.get_json()
   product_id=req_data['product_id']
   res_data=sample3.add_to_list(product_id)
   if res_data is None:
      response = Response("{'error': 'Item not added - '}"  + product_id, status=400 , mimetype='application/json')
      return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

@app.route('/items/all')
def get_all_items():
   res_data = sample3.get_all_items()
   response = Response(json.dumps(res_data), mimetype='application/json')
   return response

@app.route('/item/update', methods = ['PUT'])
def update_status():
   req_data = request.get_json()
   product_id = req_data['product_id']
   product_quantity = req_data['product_quantity']
   res_data = sample3.update_status(product_id,product_quantity)
   if res_data is None:
      response = Response("{'error': 'Error updating item - '" + product_id +  "}", status=400 , mimetype='application/json')
      return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

@app.route('/item/sell', methods = ['PUT'])
def update_status1():
   req_data = request.get_json()
   product_id = req_data['product_id']
   product_soldquantity = req_data['product_soldquantity']
   product_sellprice=req_data['product_sellprice']
   res_data = sample3.update_solditem(product_id,product_soldquantity,product_sellprice)
   if res_data is None:
      response = Response("{'error': 'Error updating item - '" + product_id +  "}", status=400 , mimetype='application/json')
      return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

@app.route('/item/remove', methods = ['DELETE'])
def delete_item():
   req_data = request.get_json()
   product_id = req_data['product_id']
   res_data = sample3.delete_item(product_id)
   if res_data is None:
      response = Response("{'error': 'Error deleting item - '" + product_id +  "}", status=400 , mimetype='application/json')
      return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response
