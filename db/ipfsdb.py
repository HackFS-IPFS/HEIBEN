import requests
import json
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
def add(Path):
    url = f'https://ipfs.infura.io:5001/api/v0/add?pin=false'
    payload = {'file':Path}
    headers =  {'Content-Type':'multipart/form-data'}
    p=requests.post(url=url,data=payload,headers=headers)
    print(p.url)
    print(p.content)

if __name__ == '__main__':
    add(f'D:\\1.json')
