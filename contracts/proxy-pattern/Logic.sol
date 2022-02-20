// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Logic {
    bytes32 myBytes;

    constructor(){
        myBytes = "HelloWorld";
    }

    function getMyBytes() external view returns(bytes32){
        return myBytes;
    }

    function setMyBytes(bytes32 _myBytes) external {
        myBytes = _myBytes;
    }
}
