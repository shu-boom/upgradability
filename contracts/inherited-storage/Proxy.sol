// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./CommonStorage.sol";

contract Proxy is CommonStorage{

    constructor() {
        owner = msg.sender;
    }

    function upgradeTo(address _implementation) public {
        require(msg.sender == owner, "Only Owner");
        implementation = _implementation;
    }

    fallback() external{
        implementation = getImplementationAddress();
        assembly {
            let ptr:=mload(0x40)
            calldatacopy(ptr, 0, calldatasize())
            let result := delegatecall(
                gas(),
                sload(implementation.slot),
                ptr,
                calldatasize(),
                0,
                0
            )
            returndatacopy(ptr, 0, returndatasize())
            switch result
            case 0 { revert(ptr, returndatasize()) }
            default { return(ptr, returndatasize()) }
        }
    }
}