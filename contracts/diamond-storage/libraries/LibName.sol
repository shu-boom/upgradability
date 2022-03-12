// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
library LibName{
    struct USER {
        string name;
    }

    function getLibNameStorage() internal pure returns(USER storage ds){
        bytes32 position = keccak256("diamond.storage.LibName");
        assembly{
            ds.slot := position
        }
    }

    function getName() internal view returns(string memory){
        USER storage _user = getLibNameStorage();
        return _user.name;
    }
    
    function setName(string memory name) internal{
         USER storage _user = getLibNameStorage();
         _user.name = name;
    }
}