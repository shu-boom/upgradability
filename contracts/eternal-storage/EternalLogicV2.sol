// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./libraries/EternalLogicLibrary.sol";

contract EternalLogicV2 {
    using EternalLogicLibrary for address; 
    address public _storage; 
    
    constructor(address __storage){
        _storage = __storage;
    }

    modifier onlyOwner {
        require(msg.sender == _storage.getOwner(), "Only Owner");
        _;
    }
    
    function getUserAge() external view returns(uint256){
        return _storage.getUserAge();
    }

    function getUserName() external view returns(string memory) {
        return _storage.getUserName();
    }   
    
    function setUserAge(uint256 age) onlyOwner external{
         _storage.setUserAge(age);
    }

    function setUserName(string memory name) onlyOwner external {
         _storage.setUserName(name);
    }   
}