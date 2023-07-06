from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "a post", "content": "This c is the first post."},
    {"id": 2, "title": "b post", "content": "This a is the second post."},
    {"id": 3, "title": "c post", "content": "This b is the third post."},
]


@app.route('/api/posts', methods=['GET', 'POST', 'PUT'])
def get_posts():
    if request.method == 'GET':
        sort = request.args.get('sort')
        direction = request.args.get('direction')
        if sort == None or direction == None:
            return jsonify(POSTS)
        else:
            if sort == 'title':
                sorted_list = sorted(POSTS, key=lambda x: x['title'])
                if direction == 'desc':
                    sorted_list.reverse()
                return jsonify(sorted_list)
            else:
                sorted_list = sorted(POSTS, key=lambda x: x['content'])
                if direction == 'desc':
                    sorted_list.reverse()
                return jsonify(sorted_list)

    elif request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        if title == None or content == None:
            error_message = {'error': 'All data fields must be provided'}
            return jsonify(error_message), 400 
        id_list = []
        for post in POSTS:
            id_list.append(post['id'])
        for number in range(10000000):
            if number not in id_list:
                unique_id = number
                break
        new_post = {"id": unique_id, "title": title, "content": content}
        POSTS.append(new_post)
        return jsonify(new_post)
    elif request.method == 'PUT':
        data = request.get_json()
        post_id = int(request.args.get('id'))
        for index, post in enumerate(POSTS):
            if post['id'] == post_id:
                edit_post = post
                del POSTS[index]
                break
            if POSTS[index]['title'] == POSTS[-1]['title']:
                return jsonify({'error': f'Post with id: {post_id} could not be found'}), 400
        if 'title' in data:
            edit_post['title'] = data['title']
        if 'content' in data:
            edit_post['content'] = data['content']
        POSTS.append(edit_post)
        return jsonify(edit_post)
    
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    for index, post in enumerate(POSTS):
        if post['id'] == post_id:
            del POSTS[index]
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    return jsonify({'error': f'Post with id: {post_id} could not be found'}), 400
    
@app.route('/api/posts/search')
def search():
    title_search = request.args.get('title')
    content_search = request.args.get('content')
    matches = []
    if title_search == None:
        title_search = ""
    if content_search == None:
        content_search = ""
    for post in POSTS:
        if content_search in post['content'] and title_search in post['title']:
            matches.append(post)
    return jsonify(matches)
       


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
