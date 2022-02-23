// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./../../interfaces/simple-interface/ILogic.sol";

contract SatelliteContractV2 is ILogic {

    ILogic.User logic;
    function getFirstName() override(ILogic) external view returns(bytes32){
        return logic.firstName;
    } 

    function getLastName() override(ILogic) external view returns(bytes32){
        return logic.lastName;
    }

    function setFirstName(bytes32 _firstName) override(ILogic) external{
        logic.firstName = _firstName;
    }

    function setLastName(bytes32 _lastName) override(ILogic) external{
        logic.lastName = _lastName;
    }
}