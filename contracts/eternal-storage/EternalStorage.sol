// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EternalStorage {
    mapping(bytes32 => address) _addressStorage;
    mapping(bytes32 => uint256) _uintStorage;
    mapping(bytes32 => string) _stringStorage;

    function getUint(bytes32 key) public view returns (uint256) {
      return _uintStorage[key];
    }

    function getAddress(bytes32 key) public view returns (address) {
      return _addressStorage[key];
    }

    function getString(bytes32 key) public view returns (string memory) {
      return _stringStorage[key];
    }

    function setUint(bytes32 key, uint256 value) public {
        _uintStorage[key] = value;
    }
    
    function setAddress(bytes32 key, address value) public {
        _addressStorage[key] = value;
    } 
    
    function setString(bytes32 key, string memory value) public {
        _stringStorage[key] = value;
    }
    
}