// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library LibAge {
    struct USER {
        uint8 age;
    }

    function getLibAgeStorage() internal pure returns(USER storage ds){
        bytes32 position = keccak256("diamond.storage.LibAge");
        assembly{
            ds.slot := position
        }
    }

    function getAge() internal view returns(uint8){
        USER storage _user = getLibAgeStorage();
        return _user.age;
    }
    
    function setAge(uint8 age) internal{
         USER storage _user = getLibAgeStorage();
         _user.age = age;
    }
}