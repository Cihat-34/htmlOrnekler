from flask import Flask, jsonify, request

app = Flask(__name__)

products = []

@app.route('/api/products', methods=['GET'])
def list_products():
    return jsonify(products), 200

@app.route('/api/products', methods=['POST'])
def create_product():
    product = request.get_json()
    
    if 'name' not in product or 'price' not in product or 'description' not in product:
        return jsonify({'error': 'Name, price, and description are required'}), 400
    product['id'] = len(products) + 1
    products.append(product)
    return jsonify(product), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product:
        data = request.get_json()
        product.update(data)
        return jsonify(product), 200
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)