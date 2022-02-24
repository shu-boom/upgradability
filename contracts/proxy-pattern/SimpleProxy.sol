
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleProxy {
    address implementation;
    address owner;
    constructor(){
        owner = msg.sender;
    }

    function getImplementationAddress() public view returns(address){
        return implementation;
    }

    function setImplementationAddress(address _implementation) public {
        require(msg.sender==owner, "Owner only");
        implementation = _implementation;
    }

    fallback() external{
        assembly {
            let ptr:=mload(0x40) // 0x40 is a special location in the EVM which manages the next free available pointer. Remember that EVM word size is 32bytes. and mload returns the 32byte free memory address
            calldatacopy(ptr, 0, calldatasize()) // ptr contains the memory location. We copy all the call data using the calldatacopy function to ptr. This includes the functionsignature and arguments padded to 32 bytes. 
            let response := delegatecall( //this function delegates the calls to the implementation address
                gas(), // the amount of gas left for the implementation contract to use to execute the given function call copied to the memory address ptr
                sload(implementation.slot), //implementation is stored as an address in memory at some address. The .slot method returns the memory location of that address and then we use sload to add the contents of together 
                ptr, //ptr is the function data that we supposed to call at the implementation address
                calldatasize(), // pass the calldatasize
                0, // this is out parameter
                0 // this is outSize parameter. They help in specifying the memory location of the returned data. 
            )
            returndatacopy(ptr, 0, returndatasize()) // copy the return data to the memory location pointer as the response of the delegate call
            switch response //delegate call only returns boolean using which we decide to return or revert
            case 0 { revert(ptr, returndatasize()) }
            default { return(ptr, returndatasize()) }
        }
    }
}

