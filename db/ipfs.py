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

    url = f"https://ipfs.infura.io:5001/api/v0/cat?arg={Hash}"
    try:
        re=requests.get(url,proxies=proxies)
    except:
        return 0
    
    a = str(re.content,'utf-8')
    return json.loads(a)

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
   


class Content:
    '''
    if you want to add some content to ipfs, please give all agurment.
    '''
    def __init__(self,productID,productName,companyName,productionDate,materialsID):
        self.productID=productID
        self.productName = productName
        self.companyName = companyName
        self.productionDate = productionDate
        self.materialsID = materialsID
    '''
    this function is add content to the IPFS network by infura network
    input： content instance
    output : IPFS Hash
    '''
    def addtoIPFS(self):
        url = f'https://ipfs.infura.io:5001/api/v0/add?pin=true'
        # check companyName,productionData,productName and materialID is not null
        if(not self.companyName or not self.productionDate or not self.productName or not self.productID):
            raise NotImplementedError('the argument companyName,productionData,productName,productID is nessasary.')

        content = {"productID":self.productID,"productName":self.productName,"companyName":self.companyName,"productionDate":self.productionDate,"materialsID":self.materialsID}
        Data = {"upload":('db.json',str(content))}
        try:
            p=requests.post(url, files=Data)
        except:
            return 0   
        return json.loads(str(p.content,'utf-8'))['Hash']
    '''
    this function get content from ipfs from infura network
    input : ContentHash
    output : content
    '''
    def get(self,ContentHash):
        url = f"https://ipfs.infura.io:5001/api/v0/cat?arg={ContentHash}"
        try:
            re=requests.get(url,proxies=proxies)
        except:
            return 0
    
        a = json.loads(str(re.content,'utf-8').replace('\'','\"'))
        self.productID=a['productID']
        self.productionDate=a['productionDate']
        self.productName = a['productName']
        self.companyName = a['companyName']
        self.materialsID = a['materialsID']
        return self

if __name__ == '__main__':
    content = Content("Example","producNameExample","companyNameExample","2010-01-0",["material1","material2"])
    addr = content.addtoIPFS()
    print(addr)
    # QmUcgXXC473q6UiuyzpsutPs4T68tadkoJnXbpcj5EF4Vx
    content_tmp = Content("","","","",[])
    print(content_tmp.get('QmUcgXXC473q6UiuyzpsutPs4T68tadkoJnXbpcj5EF4Vx'))


        
        