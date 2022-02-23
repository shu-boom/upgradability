// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "./LogicV1.sol";

contract LogicV2 is LogicV1 {
    uint256 internal age;

    function getAge() external view returns(uint256){
        return age;
    }

    function setAge(uint256 _age) external {
        age = _age;
    }
}