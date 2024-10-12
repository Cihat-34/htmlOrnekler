from flask import Flask,jsonify,request

app = Flask(__name__)

users = []

@app.route('/api/users', methods = ['GET'])
def list_users():
    return jsonify(users),200

@app.route('/api/users',methods = ['POST'])
def create_user():
    user = request.get_json()
    if 'name' not in user or 'email' not in user:
        return jsonify({'error':'Name and email are required'}),400
    user['id'] = len(users) + 1
    users.append(user)
    return jsonify(user),201

@app.route('/api/users/<int:user_id>',methods = ['PUT'])
def update_user():
    user = next((user for user in users if user['id'] == 'user_id'),None)
    if user:
        data = request.get_json()
        user.update(data)
        return jsonify(user)
    return jsonify({'error' : 'User not found'}),404

if __name__ == '__main__':
    app.run(debug=True,port=8000)