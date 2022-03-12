// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TestReplace {
    function facetAddress(bytes4 _functionSelector) external view returns (address facetAddress_){
        facetAddress_= msg.sender;
    }
}