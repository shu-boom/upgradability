// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./../../interfaces/simple-interface/ILogic.sol";


contract MainContract {
    address owner;
    ILogic satteliteContract;
    constructor() {
        owner = msg.sender;
    }

    function upgradeTo(address newImplementation) public {
        require(msg.sender == owner, "Only Owner");
        satteliteContract = ILogic(newImplementation);
    }
    
    function getFirstName() external returns(bytes32){
        return satteliteContract.getFirstName();
    } 

    function getLastName() external returns(bytes32){
        return satteliteContract.getLastName();
    }

    function setFirstName(bytes32 _firstName) external {
        satteliteContract.setFirstName(_firstName);
    }

    function setLastName(bytes32 _lastName)  external{
        satteliteContract.setLastName(_lastName);
    }
}