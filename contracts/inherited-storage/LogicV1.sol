// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./CommonStorage.sol";

contract LogicV1 is CommonStorage {

    function getFirstName() external view returns(string memory){
        return firstName;
    }

    function getLastName() external view returns(string memory){
        return lastName;
    }

    function setFirstName(string calldata _firstName) external {
        firstName = _firstName;
    }

    function setLastName(string calldata _lastName) external {
        lastName = _lastName;
    }
}