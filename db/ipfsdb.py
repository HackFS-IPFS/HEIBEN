import pycurl
import certifi
from io import BytesIO
import requests

c = pycurl.Curl()
#因为我本地的vpn转发端口在1080，可更换
c.setopt(pycurl.PROXY,'127.0.0.1:1080')
c.setopt(pycurl.CAINFO, certifi.where())
buffer = BytesIO()

def get(DataHash):
    
    url = f'https://ipfs.infura.io:5001/api/v0/get?arg={DataHash}&archive=true'
    c.setopt(pycurl.URL, url)
    c.setopt(c.WRITEDATA, buffer) 
    try:
        c.perform()
        re = str(buffer.getvalue())
    except:
        return 0
    return  re


if __name__ == '__main__':
    get('QmdSaxi2xGHpnTyvMtNDgLVtewknmtCm7ot7MgptUQWqvy')
