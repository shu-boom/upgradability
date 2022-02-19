// SPDX-License-Identifier: MIT
// An interface is like the contract ABI in Solidity.
// The motivation for interfaces 
// An interface can only contain external methods.
// It can only inherit from other interfaces. 
// They do not have their own storage. Therefore, state variables are not allowed
// They can have user-defined types such as Struct and Enums.'
// They can have event declaration.
// A base contract can only implement some of the interface methods. 
// Interfaces allows one contract to communicate with othercontracts that implement the interface. 

pragma solidity ^0.8.0;

interface ILogic {
    struct User{
        bytes32 firstName;
        bytes32 lastName;
    }
    function getFirstName() external returns(bytes32);
    function getLastName() external returns(bytes32);
    function setFirstName(bytes32 _firstName) external;
    function setLastName(bytes32 _lastName) external;
}