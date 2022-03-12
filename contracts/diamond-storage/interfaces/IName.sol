// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IName {
    function getUserName() external returns(string memory);
    function setUserName(string memory name) external;
}