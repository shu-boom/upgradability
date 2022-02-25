// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UnstructuredLogicV1 {
    uint256 val;

    function getVal() external view returns(uint256) {
        return val;
    }

    function setVal(uint256 _newVal) external {
        val = _newVal;
    }
}