from flask import *
from ethereum.ethereum import Ethereum
import db.ipfs
import traceback
from flask_cors import CORS
from flask import render_template #引入模板插件

app = Flask(__name__, static_folder='../frontEnd/dist/static',  #设置静态文件夹目录
template_folder = "../frontEnd/dist")

CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return render_template('index.html',name='index') #使用模板插件，引入index.html。此处会自动Flask模板文件目录寻找index.html文件。

'''
temporary function for login
input: none
output: {"code": 20000, "data": {"token": "admin-token"}}
'''


@app.route('/api/user/login/', methods=["POST"])
def login():
    data = {"code": 20000, "data": {"token": "admin-token"}}
    return json.dumps(data)


'''
temporary function for user info
input: productID
output: always
'''


@app.route('/api/user/logout/', methods=["POST"])
def logout():
    data = {"code": 20000, "data": "success"}
    return json.dumps(data)


'''
temporary function for for user info
input: productID
output: always
'''


@app.route('/api/user/info/', methods=["GET"])
def getInfo():
    data = {"code": 20000, "data": {"roles": ['admin'], "introduction": 'I am a super administrator',
            "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif', "name": 'Super Admin'}}
    return json.dumps(data)


'''
this function read productID and return the correspondent items
input: productID
output: json of items
(if the materials of one products doesn't exist, a json which only contains its ID will be returned. )
'''


@app.route('/api/trace/', methods=["GET"])
def traceById():
    productID = request.args.get("productID")
    result = []
    if not isinstance(productID, str):
        return make_response("argument productID should be str!", 404)
    productList = [productID]
    ethereum = Ethereum()
    ethereum.get_contract_instance("0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836")
    while len(productList) > 0:
        curID = productList.pop()
        ipfsAddress = ethereum.getHash(curID)
        if ipfsAddress == "false":
            print("curID " + curID + " is missing")
            result.append({"productID": curID})
            continue
        print(ipfsAddress)
        Itemdata = db.ipfs.Content.get(ipfsAddress)
        for materialID in Itemdata["materialsID"]:
            productList.insert(0, materialID)
        result.append(Itemdata)
    print(result)
    if len(result) == 1 and result[0].keys() == 1:
        response = make_response("The productID " + productID + "is not found", 404)
    else:
        response = make_response(jsonify(result), 200)
    return response


'''
this function accept the json file and upload it to the IPFS
input: json of item
output: error message and statues code
'''


@app.route('/api/add/', methods=["POST"])
def addById():
    newData: dict = json.loads(request.get_data())
    content: db.ipfs.Content = None
    try:
        content = db.ipfs.Content(newData)
    except Exception:
        print(traceback.print_exc())
        return make_response("format Error", 404)
    ipfsAddr = content.addtoIPFS()
    if not isinstance(ipfsAddr, str):
        return make_response("Error when add to IPFS", 404)
    print("ipfsAddr has been added: ", ipfsAddr)
    ethereum = Ethereum()
    ethereum.get_contract_instance("0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836")
    ethereum.newHash(ipfsAddr)
    ethereum.newRelation(content.productID, ipfsAddr)
    print(ethereum.getHash(content.productID) == ipfsAddr)
    # print(productID)
    # print(ethereum.getHash(productID))
    # # 建立新关
    return make_response("upload success", 200)


if __name__ == "__main__":
    app.run(debug=True)
