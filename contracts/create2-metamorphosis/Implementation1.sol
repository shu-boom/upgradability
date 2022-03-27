// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Implementation1 {
    uint public integer;

    function setInteger(uint _integer) public {
        integer = _integer;
    }

    function destruct() external {
        selfdestruct(payable(msg.sender));
    }
}

