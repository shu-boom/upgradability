// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "./LogicV1.sol";

contract LogicV2 is LogicV1 {
    uint8 internal age;

    function getAge() external view returns(uint8){
        return age;
    }

    function setAge(uint8 _age) external {
        age = _age;
    }
}