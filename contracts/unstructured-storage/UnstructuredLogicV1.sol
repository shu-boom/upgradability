// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UnstructuredLogicV1 {
    uint256 val;
    // Tip public function may be called internally; therefore, solidity copies the arguments for a public function to memory. Whereas, external functions are cheap 
    // because they rely on calldata instead of memory 
    function getVal() external view returns(uint256) {
        return val;
    }

    function setVal(uint256 _newVal) external {
        val = _newVal;
    }
}