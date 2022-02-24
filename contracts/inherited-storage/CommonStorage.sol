// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract CommonStorage {
    address internal implementation;
    address internal owner;
    string internal firstName;
    string internal lastName;
    /*
    * Returns the implementation address
    */
    function getImplementationAddress() public view returns(address){
        return implementation;
    }

}