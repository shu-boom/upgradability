// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract CommonStorage {
    address internal implementation;
    address internal owner;
    bytes32 internal firstName;
    bytes32 internal lastName;
    /*
    * Returns the implementation address
    */
    function getImplementation() public view returns(address){
        return implementation;
    }

}