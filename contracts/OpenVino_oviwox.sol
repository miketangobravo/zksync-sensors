// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IotStoreData {
    address public owner;
    mapping(uint256 => string) private dataStorage;
    mapping(uint256 => uint256) private timestamps;
    mapping(address => bool) public authorizedUpdaters;
    uint256 private currentId = 0;
    uint256[] private dataIds;

    event DataStored(uint256 indexed id, uint256 timestamp, string data, address updater);
    event UpdaterAuthorized(address updater);
    event UpdaterRevoked(address updater);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    modifier onlyAuthorized() {
        require(msg.sender == owner || authorizedUpdaters[msg.sender], "Not authorized");
        _;
    }


    function authorizeUpdater(address updater) public onlyOwner {
        authorizedUpdaters[updater] = true;
        emit UpdaterAuthorized(updater);
    }

 
    function revokeUpdater(address updater) public onlyOwner {
        authorizedUpdaters[updater] = false;
        emit UpdaterRevoked(updater);
    }


    function storeData(string memory data) public onlyAuthorized {
        uint256 id = currentId++;
        uint256 timestamp = block.timestamp;
        
        dataStorage[id] = data;
        timestamps[id] = timestamp;
        dataIds.push(id);

        emit DataStored(id, timestamp, data, msg.sender);
    }

  
    function getData(uint256 id) public view returns (string memory) {
        return dataStorage[id];
    }

  
    function getTimestamp(uint256 id) public view returns (uint256) {
        return timestamps[id];
    }

    
    function getAllData() public view returns (string[] memory) {
        uint256 length = dataIds.length;
        string[] memory allData = new string[](length);

        for (uint256 i = 0; i < length; i++) {
            allData[i] = dataStorage[dataIds[i]];
        }

        return allData;
    }

   
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "New owner cannot be the zero address");
        owner = newOwner;
    }
}
