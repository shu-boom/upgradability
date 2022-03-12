// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IAge {
    function getUserAge() external returns(uint8);
    function setUserAge(uint8 age) external;
}