from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "a post about dogs", "content": "This is the first post about a dog."},
    {"id": 4, "title": "Flask", "content": "This is a post about flask"},
    {"id": 5, "title": "Test", "content": "this post is about testing"},
    {"id": 6, "title": "nothing really", "content": "this post is just for fun"},
    ]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    this function is creating a list of all the posts in the blog.
    it allows sorting by title/content and ascending/descending order.
    if the user doesn’t provide the sorting parameters,
    it returns posts in their original order.
    """
    sort_by = request.args.get('sort')
    direction = request.args.get('direction')

    if sort_by and sort_by not in ['title', 'content']:
        return jsonify(error='Invalid sort field'), 400

    if direction and direction not in ['asc', 'desc']:
        return jsonify(error='Invalid sort direction'), 400

    def sort_posts(posts, sort_by, direction):
        """ this is a helper function that sorts the posts. """
        if not sort_by or not direction:
            return posts

        return sorted(posts, key=lambda post: post[sort_by].lower(), reverse=(direction == 'desc'))

    return jsonify(sort_posts(POSTS, sort_by, direction))


@app.route('/api/posts', methods=['POST'])
def add_post():
    """ this function is creating a new post in the blog. """
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify(error='Missing title or content'), 400

    title = data['title']
    content = data['content']

    # Create a new post ID
    if len(POSTS) > 0:
        last_post = POSTS[-1]
        last_post_id = last_post["id"]
        post_id = last_post_id + 1
    else:
        post_id = 1

    # Create a new post dictionary
    new_post = {
        "id": post_id,
        "title": title,
        "content": content
    }
    # Add the new post to the list
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=["DELETE"])
def delete_post(post_id):
    """ this function is deleting an existing post from the blog. """
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify(message=f"Post with id {post_id} has been deleted successfully."), 202
    return jsonify(error=f"Post with id {post_id} not found."), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """ this function is updating the content/title of an existing post. """
    data = request.get_json()
    if not data:
        return jsonify(error='No data provided'), 400

    for post in POSTS:
        if post['id'] == post_id:
            if 'title' in data:
                post['title'] = data['title']
            if 'content' in data:
                post['content'] = data['content']
            return jsonify(post), 200

    return jsonify(error=f"Post with id {post_id} not found."), 404


@app.route('/api/posts/search', methods=['GET'])
def search():
    """ this function is searching for posts in the blog
    by it's content or title. """
    args = request.args
    title_search = args.get('title')
    content_search = args.get('content')

    matching_posts = []
    for post in POSTS:
        if title_search and title_search in post['title']:
            matching_posts.append(post)
        elif content_search and content_search in post['content']:
            matching_posts.append(post)

    return jsonify(matching_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
