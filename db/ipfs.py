import requests
import json
# import pycurl
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "127.0.0.1:1080",
}
'''
this function search hash in IPFS network and return the content required by hash
input:  Hash:String
output: Content:Json
'''
def get(Hash):

    try:
        re=requests.get("https://ipfs.infura.io:5001/api/v0/cat?arg={Hash}",proxies=proxies)
    except:
        return 0

    return re.content.json()

'''
This function upload file required by the file path and return the file hash
input: Path:String
output: Hash:String
'''
def addContentbyPath(Path):
    url = f'https://ipfs.infura.io:5001/api/v0/add?pin=false'
    with open(Path,'rb') as f:
        files = {"upload":(Path,f)}
        try:
            p = requests.post(url, files=files)
        except:
            return 0
        return json.loads(str(p.content,'utf-8'))['Hash']
    
'''
this function add Content to IPFS by suporting the data of dict or bytes or string
input : Data : str|dict|bytes
output: Hash: String
'''
def addContent(Data):
    url = f'https://ipfs.infura.io:5001/api/v0/add?pin=false'
    if type(Data)==dict or bytes:
        Data = str(Data)
    try:
        files = {"upload":('db.json',Data)}
        p=requests.post(url, files=files)

    except:
        return 0
    return json.loads(str(p.content,'utf-8'))['Hash']
   
if __name__ == '__main__':
    addContentbyPath('D:\\1.json')
