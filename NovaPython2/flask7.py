from flask import Flask, jsonify, request
app = Flask(__name__)

comments = []

@app.route('/api/comments', methods=['GET'])
def list_comments():
    return jsonify(comments), 200

@app.route('/api/comments', methods=['POST'])
def create_comment():
    comment = request.get_json()
    if 'post_id' not in comment or 'author' not in comment or 'content' not in comment:
        return jsonify({'error': 'Post ID, author, and content are required'}), 400
    
    comment['id'] = len(comments) + 1
    comments.append(comment)
    return jsonify(comment), 201

@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = next((c for c in comments if c['id'] == comment_id), None)
    
    if comment:
        data = request.get_json()
        
        comment.update(data)
        return jsonify(comment), 200
    return jsonify({'error': 'Comment not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)