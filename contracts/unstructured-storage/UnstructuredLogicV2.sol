// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UnstructuredLogicV2 {
    uint256 val;
    uint256 newVal;

    function getVal() external view returns(uint256) {
        return newVal;
    }

    function setVal(uint256 _newVal) external {
        newVal = _newVal;
    }
}