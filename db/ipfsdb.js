const IPFS = require('ipfs-api');
const ipfs = new IPFS({ host: 'ipfs.infura.io', port: 5001, protocol: 'https' });

function FindItemByHash(IDHash)
{
    var address = 'https://ipfs.infura.io:5001/api/v0/get?arg=${IDHash}';
    var result  = ipfs.get(address);
    return result;
}

function Add(Data)
{
    var object = ipfs.add(Data);
    return object[Hash];
}


