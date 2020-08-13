# HEIBEN
item traceability system based on ipfs and eth
## front-end
1. install Solidity(v0.4.25)
https://www.cnblogs.com/StephenWu/p/6791490.html
```
npm install -g solc@0.4.25
```
2. install the frontEnd package
```access transformers
cd frontEnd
npm install
```
## back-end
3. build front end
```access transformers
npm run build:prod
```

4. install python dependencies
```access transformers
cd backEnd
pip install -r pipreq.txt 
```
5.  deploy the website
```access transformers
cd backEnd
python main.py
(use --proxyPort to specify the port of proxy,e.g.
python main.py --proxyPort 8000)
```


文档工程师还在赶来修文档的路上^V^
