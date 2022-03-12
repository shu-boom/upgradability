// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/* 
    This is a diamond cut interface. This interface is used to specify the structure of the Diamond contract and storage. 
*/

 interface IDiamondCut{
     // An ENUM that stores the required action. 
    enum FacetAction {
        ADD,
        REPLACE,
        REMOVE
    }

    // This is a struct for each facet. Each facet has many selectors. 
    struct FacetCut {
        address facetAddress;
        bytes4[] selectors;
        FacetAction action;
    }
    // @notice This function upgrades modifies the selectors of a facet
    // Emits an event when the modification is completed for offchain providers to use. 
    // params _facets: A facet array for holding a struct
    // params _init: The address of the contract or facet to execute _calldata
    // params _calldata: TBD
    function diamondCut(FacetCut calldata  _facet, bytes calldata _calldata, address _init) external;
   
    // every time a diamondCut function is executed a diamond cut event is emitted.
    event DiamondCut(FacetCut _facet, bytes _calldata, address _init);
    event addedSelector(bytes4 selector, address _facetAddress, bytes4[] selectors, address _facetAddressForSelector, uint16 selectorIndex);

    // event FacetAddress(address facet);
    // event AddSelectorEvent(address facet, bytes4 selector);
 }