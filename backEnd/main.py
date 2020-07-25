from flask import *
app = Flask(__name__)
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

@app.route('/api/trace/',methods=["GET"])
def traceById():
    id =  request.args.get("id")
    # show the subpath after /path/

    response = make_response(jsonify({'test': 'good'}),403)
    return response
if __name__ == "__main__":
    app.run(debug = True)