// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./../interfaces/ILogic.sol";


contract MainContract {
    address owner;
    ILogic satteliteContract;
    constructor() {
        owner = msg.sender;
    }
    function upgradeTo(address newImplementation) public {
        require(msg.sender == owner, "Only Owner");
        satteliteContract = ILogic(newImplementation);
    }
}