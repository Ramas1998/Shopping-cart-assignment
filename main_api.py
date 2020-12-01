import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

'''@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp


@app.route("/api/v1/cart_items", methods=['POST'])
def create_items():
    """
       Function to create new users.
       """
    try:
        # Create new users
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        record_created = collection.insert(body)'''

def dict_factory(cursor, row): 
	"""Converts rows that need to be retrieved into a dictionary object. This function replaces the existing row_factory attribute of the sqlite3 connection object.z"""
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

@app.route('/', methods=['GET'])
def home():
	"""This is the home page of the API."""
	return "<h1>Shopify Backend assignment</h1><p>This site is a prototype for shopping cart API.</p>"


@app.route('/cart_items/all', methods=['GET']) 
def api_all():
	"""Displays all the products present in the database."""
	conn = sqlite3.connect('collections.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	all_products = cur.execute('SELECT * FROM products WHERE inventory_count>0;').fetchall()
	return jsonify(all_products)

@app.route('/cart_items', methods=['GET'])
def api_search():
	"""Search for products on the basis of 'id' or 'title' values.Eg: Use /cart_items?id=3 to search for the product whose id equals to 3."""
	if 'id' in request.args:
		id = int(request.args['id'])
		flag_id=1
		flag_title=0
	elif 'title' in request.args:
		title = request.args['title']
		flag_title=1
		flag_id=0
	else:
		return "Error: No id/title field provided. Please specify an id/title."

		conn = sqlite3.connect('collections.db')
		conn.row_factory = dict_factory
		cur = conn.cursor()
		# Create an empty list for our results
	if flag_id==1:
		t = (id,)
		products = cur.execute('SELECT * FROM products WHERE id=? ',t).fetchone()
		return jsonify(products)
	else:
		t = (title,)
		products = cur.execute('SELECT * FROM products WHERE title=? ',t).fetchone()
		return jsonify(products)

'''@app.route("/api/v1/cart_items", methods=['GET'])
def fetch_users():
    """
       Function to fetch the users.
       """
    try:
        # Call the function to get the query params
        query_params = helper_module.parse_query_params(request.query_string)
        # Check if dictionary is not empty
        if query_params:

            # Try to convert the value to int
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}

            # Fetch all the record(s)
            records_fetched = collection.find(query)

            # Check if the records are found
            if records_fetched.count() > 0:
                # Prepare the response
                return dumps(records_fetched)
            else:
                # No records are found
                return "", 404

        # If dictionary is empty
        else:
            # Return all the records as query string parameters are not available
            if collection.find().count() > 0:
                # Prepare response if the users are found
                return dumps(collection.find())
            else:
                # Return empty array if no users are found
                return jsonify([])
    except:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/cart_items/<item_id>", methods=['POST'])
def update_cart(item_id):
    """
       Function to update the user.
       """
    try:
        # Get the value which needs to be updated
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return "", 400

        # Updating the user
        records_updated = collection.update_one({"id": int(item_id)}, body)

        # Check if resource is updated
        if records_updated.modified_item > 0:
            # Prepare the response as resource is updated successfully
            return "", 200
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return "", 404
    except:
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/cart_items/<item_id>", methods=['DELETE'])
def remove_user(item_id):
    """
       Function to remove the user.
       """
    try:
        # Delete the user
        delete_item = collection.delete_one({"id": int(item_id)})

        if delete_item.deleted_count > 0 :
            # Prepare the response
            return "", 204
        else:
            # Resource Not found
            return "", 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp
'''
@app.route('/cart_items/add',methods=['GET'])
def api_add_cart():
	"""Add products to the cart based on the id provided. Eg: Use /cart_items/add?id=2 to add product whose id equals 2."""
	if 'id' in request.args:
		id = int(request.args['id'])
	else:
		return "Error: No id field provided. Please specify an id."

	conn = sqlite3.connect('collections.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS cart(id real PRIMARY KEY, title text, inventory_count real, price real)''')
	count= cur.execute('SELECT COUNT(*) FROM cart WHERE id=? ',(id,)).fetchone()
	#print(count)
	if count['COUNT(*)']>=1:
		return "Already in the cart"
	else:
		record = cur.execute('SELECT * FROM products WHERE products.id=?',(id,)).fetchone()
		if record==None:
			return "No such product exists"
		cur.execute('INSERT INTO cart VALUES(?,?,?,?)',(record['id'],record['title'],record['inventory_count'],record['price']))
		conn.commit()
		return "Item has been added to the cart"

@app.route('/cart_items/',methods=['GET'])
def api_display_cart():
	"""Display all the products present in the cart."""
	conn = sqlite3.connect('collections.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	cart = cur.execute('SELECT * FROM cart;').fetchall()
	cart.append(cur.execute('SELECT SUM(price) from cart;').fetchone())
	return jsonify(cart)

@app.route('/cart_items/delete',methods=['GET'])
def api_delete_cart():
	"""Delete products from the cart based on the id provided. Eg: Use /v1/cart/delete?id=2 to delete product from cart whose id equals to 2."""
	if 'id' in request.args:
		id = int(request.args['id'])
	else:
		return "Error: No id field provided. Please specify an id."

	conn = sqlite3.connect('collections.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	count= cur.execute('SELECT COUNT(*) FROM cart WHERE id=? ',(id,)).fetchone()
	if count['COUNT(*)']==0:
		return "Error:The item you want to delete is not available in the cart"
	else:
		cur.execute('DELETE FROM cart WHERE id=?',(id,))
		conn.commit()
		return 'Successfully deleted the item'


app.run()
