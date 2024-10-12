from flask import Flask,jsonify,request
app = Flask(__name__)
tasks = []

@app.route('/api/tasks', methods = ['GET'])
def list_task():
    return jsonify(tasks),200

@app.route('/api/tasks',methods = ['POST'])
def create_task():
    task = request.get_json()
    if 'title' not in task or 'description' not in task:
        return jsonify({'error':'Title and Description are required'}),400
    task['id'] = len(tasks) + 1
    task["Completed"] = False
    tasks.append(task)
    return jsonify(task),201

@app.route('/api/users/<int:task_id>',methods = ['PUT'])
def update_task():
    task = next((task for task in tasks if task['id'] == task_id),None)
    if task:
        data = request.get_json()
        if 'title' in data:
            task['title'] = data['title']
        if 'description' in data:
            task['description'] = data['description']
        return jsonify(task),200
    return jsonify({'error' : 'Task not found'}),404

if __name__ == '__main__':
    app.run(debug=True,port=8000)
