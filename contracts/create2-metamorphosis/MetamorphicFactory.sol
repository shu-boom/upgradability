// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MetamorphicFactory {
    address implementation;
    event Deployed(address _addr);

    function deploy(bytes32 salt, bytes memory bytecode) public {
    bytes memory metamorphicCode  = (
          hex"5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"
    );
    address metamorphicContractAddress = _getMetamorphicContractAddress(salt, metamorphicCode);
    address implementationContract;
    assembly {
        let encoded_data := add(0x20, bytecode) 

        let encoded_size := mload(bytecode)  

        implementationContract := create(      
            0,                                 
            encoded_data,                         
            encoded_size                         
        )
    } 

    require(
        implementationContract != address(0),
          "Failed to deploy the new implementation contract."
    );

    implementation = implementationContract;
    address addr;

    assembly {
            let encoded_data := add(0x20, metamorphicCode) // load initialization code.
            let encoded_size := mload(metamorphicCode)     // load init code's length.
            addr := create2(0, encoded_data, encoded_size, salt)
    }

    require(
        addr == metamorphicContractAddress,
          "Failed to deploy the new metamorphic contract."
    );

    emit Deployed(addr);
    }

    /**
    * @dev Internal view function for calculating a metamorphic contract address
    * given a particular salt.
    * 
    */
    function _getMetamorphicContractAddress(
        bytes32 salt,
        bytes memory metamorphicCode
        ) public view returns (address) {

        // determine the address of the metamorphic contract.
        return address(
          uint160(                      // downcast to match the address type.
            uint256(                    // convert to uint to truncate upper digits.
              keccak256(                // compute the CREATE2 hash using 4 inputs.
                abi.encodePacked(       // pack all inputs to the hash together.
                  hex"ff",              // start with 0xff to distinguish from RLP.
                  address(this),        // this contract will be the caller.
                  salt,                 // pass in the supplied salt value.
                  keccak256(
                      abi.encodePacked(
                        metamorphicCode
                      )
                  )     // the init code hash.
                )
              )
            )
          )
        );
    }
  //those two functions are getting called by the metamorphic Contract
    function getImplementation() external view returns (address) {
        return implementation;
    }
}