// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./interfaces/IDiamondCut.sol";
import "./libraries/LibDiamond.sol";

contract Diamond is IDiamondCut {

    constructor(){
       LibDiamond.setOwner(msg.sender);
    }

   function diamondCut(FacetCut calldata  _facet, bytes calldata _calldata, address _init) external override {
        LibDiamond.enforceIsContractOwner();
        LibDiamond.diamondCut(_facet, _calldata, _init);
   }

    fallback() external {
    LibDiamond._DiamondStorage storage ds = LibDiamond.getDiamondStorage();
    address facet = ds.selectorTofacet[msg.sig]._facetAddress;
    require(facet != address(0));
    assembly {
        calldatacopy(0, 0, calldatasize())
        let result := delegatecall(gas(), facet, 0, calldatasize(), 0, 0)
        returndatacopy(0, 0, returndatasize())
        switch result
        case 0 {revert(0, returndatasize())}
        default {return (0, returndatasize())}
    }
  }
}