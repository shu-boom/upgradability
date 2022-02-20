// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Logic {
    uint256 myInt;

    constructor(){
        myInt = 10;
    }

    function getMyInt() external view returns(uint256){
        return myInt;
    }

    function setMyInt(uint256 _myInt) external {
        myInt = _myInt;
    }
}
