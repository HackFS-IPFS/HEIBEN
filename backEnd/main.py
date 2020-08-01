from flask import *
# from ethereum.ethereum import Ethereum
import db.ipfsdb
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
    # 实例化对象
    ethereum = Ethereum()
    # 初始化合约对象
    ethereum.get_contract_instance("0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836")
    ipfsAddress = ethereum.getHash(id)
    Itemsdata = db.ipfsdb.get(ipfsAddress)
    response = make_response()
    return response


@app.route('/api/add/',methods=["POST"])
def addById():
    newData = json.loads(request.get_data())
    print(newData)
    # data = json.loads(data)
    # productID =  request.form["productID"]
    # productName = request.form["productName"]
    # show the subpath after /path/
    # 实例化对象
    # ethereum = Ethereum()
    # # 初始化合约对象
    # ethereum.get_contract_instance("0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836")
    # ipfsAddress = db.ipfsdb.add("#TODO")
    #
    # print(ethereum.newHash(ipfsAddress))
    # # 建立新关系
    # print(ethereum.newRelation("123", ipfsAddres
    # s))
    response = make_response(newData)
    # print(productID)
    return response

if __name__ == "__main__":
    app.run(debug = True)
