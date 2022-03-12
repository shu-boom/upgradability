// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "../interfaces/IAge.sol";
import "../libraries/LibAge.sol";

contract ImplementationAge is IAge { 

    function initialize() external{
        LibAge.setAge(27);
    }

    function getUserAge() external override view returns(uint8) {
        return LibAge.getAge();
    }
    
    function setUserAge(uint8 age) external override {
        LibAge.setAge(age);
    }
}