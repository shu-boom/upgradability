// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./CommonStorage.sol";

contract LogicV1 is CommonStorage {

    function getFirstName() external view returns(bytes32){
        return firstName;
    }

    function getLastName() external view returns(bytes32){
        return lastName;
    }

    function setFirstName(bytes32 _firstName) external {
        firstName = _firstName;
    }

    function setLastName(bytes32 _lastName) external {
        lastName = _lastName;
    }
}