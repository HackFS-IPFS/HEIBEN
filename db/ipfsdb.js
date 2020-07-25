import pycurl
import certifi
from io import BytesIO

c = pycurl.Curl()
#因为我本地的vpn转发端口在1080，可更换
c.setopt(pycurl.PROXY,'127.0.0.1:1080')
c.setopt(pycurl.CAINFO, certifi.where())

def get(DataHash):
    url = f'https://ipfs.infura.io:5001/api/v0/get?arg={DataHash}&archive=true'
    c.setopt(pycurl.URL, url)
    try:
        re =  c.perform()
    except:
        return null
    return  re



if __name__ == '__main__':
    print(get('QmZtmD2qt6fJot32nabSP3CUjicnypEBz7bHVDhPQt9aAy')) 
