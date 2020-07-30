//pragma solidity  >=0.5.0 <0.7.0;

// author Author : Imagin
// Blog : https://imagin.vip
// Date : 2020.7.20
// Time : 18:30:17
// Contract address : 0x8d592ad6DA67C3FdDe95a3cD8c33441F29C39836


contract hackfs{
    
    mapping (string => uint) data;
    string[] hashIndex;
    
    function getHash(string memory uuid) public view returns (string memory){
        uint256 valueIndex = data[uuid];
        if (strEqual(hashIndex[valueIndex], "")) {
            return "no value";
        }
        return hashIndex[valueIndex];
    }
    
    function newHash(string memory value) public {
        uint256 i = 0;
        for(i; i < hashIndex.length; i++){
            require(!strEqual(value, hashIndex[i]), "This value already on the chain.");
            // 当前数据已经存在 
        }
        hashIndex.push(value);
    }
    
    function updateHash(string memory oldHashValue, string memory newHashValue) public {
        uint256 i = 0;
        for(i; i < hashIndex.length; i++){
            if(strEqual(oldHashValue, hashIndex[i])){
                break;
            }
        }
        // 找到索引
        require(i != hashIndex.length, "Error occured, value not found.");
        hashIndex[i] = newHashValue;
    }
    
    function newRelation(string memory uuid, string memory hashValue) public{
        require(!strEqual(hashIndex[data[uuid]], ""), "ID already exists.");
        // 当前编号已经有对应的哈希值 
        uint256 i = 0;
        for(i; i < hashIndex.length; i++){
            if(strEqual(hashValue, hashIndex[i])){
                break;
            }
        }
        // 找到索引
        require(i != hashIndex.length, "Value not found, use newHash() first.");
        // 越界了都没读到
        data[uuid] = i;
    }
    
    function hello() public pure returns (string memory){
        return "helloWorld";
    }
    
    function strEqual(string memory str1, string memory str2) internal pure returns(bool) {
        return keccak256(abi.encodePacked(str1)) == keccak256(abi.encodePacked(str2));
    }
}