
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./EternalStorage.sol";

contract EternalProxy{
    EternalStorage _storage;
    constructor(EternalStorage __storage){
        _storage = __storage;
        _storage.setAddress("owner", msg.sender);
    }

    function getImplementationAddress() public view returns(address){
        return  _storage.getAddress("implementation");
    }

    function setImplementationAddress(address _implementation) public {
        require(msg.sender==_storage.getAddress("owner"), "Owner only");
         _storage.setAddress("implementation", _implementation);
    }

    function getOwnerAddress() public view returns(address) {
            return _storage.getAddress("owner");
    }
    
    fallback() external{
        address implementation = getImplementationAddress();
        assembly {
            let ptr:=mload(0x40) 
            calldatacopy(ptr, 0, calldatasize()) 
            let response := delegatecall(
                gas(), 
                implementation, 
                ptr, 
                calldatasize(), 
                0, 
                0 
            )
            returndatacopy(ptr, 0, returndatasize()) 
            switch response 
            case 0 { revert(ptr, returndatasize()) }
            default { return(ptr, returndatasize()) }
        }
    }
}

