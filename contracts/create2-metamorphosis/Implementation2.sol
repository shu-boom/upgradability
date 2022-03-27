// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Implementation2 {
    uint public integer;

    function setInteger(uint _integer) public {
        integer = _integer * _integer;
    }

    function destruct() external {
        selfdestruct(payable(msg.sender));
    }

}