// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import ".././EternalStorage.sol";

library EternalLogicLibrary {

    function getUserAge(address _storageAddress) external view returns(uint256){
        return EternalStorage(_storageAddress).getUint("age");
    }

    function getUserName(address _storageAddress) external view returns(string memory) {
        return EternalStorage(_storageAddress).getString("name");
    }   
    
    function getOwner(address eternalStorage) external view returns(address) {
        return EternalStorage(eternalStorage).getAddress("owner");
    }

    function setUserAge(address _storageAddress, uint256 age) external{
        EternalStorage(_storageAddress).setUint("age", age);
    }

    function setUserName(address _storageAddress, string memory name) external {
        EternalStorage(_storageAddress).setString("name", name);
    }   
}