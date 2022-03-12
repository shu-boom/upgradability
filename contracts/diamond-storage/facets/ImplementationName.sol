// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "../interfaces/IName.sol";
import "../libraries/LibName.sol";

contract ImplementationName is IName {

    function initialize() external{
        LibName.setName("Boom");
    }

    function getUserName() external override view returns(string memory) {
        return LibName.getName();
    }
    
    function setUserName(string memory name) external override {
        LibName.setName(name);
    }
}