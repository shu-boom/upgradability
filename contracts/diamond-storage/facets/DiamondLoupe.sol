// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "../interfaces/IDiamondLoupe.sol";
import "../libraries/LibDiamond.sol";

contract DiamondLoupe is IDiamondLoupe {
    /// @notice Gets all facet addresses and their four byte function selectors.
    /// @return facets_ Facet
    function facets() external override view returns (Facet[] memory facets_) {
        // get the storage pointer
        LibDiamond._DiamondStorage storage ds = LibDiamond.getDiamondStorage();
        uint256 selectorCount = ds.selectors.length; // count the total number of selectors 
        // emit allSelectors(ds.selectors);
        facets_ = new Facet[](selectorCount); // _facets array equal to the selector count. If addSelector is working correctly this should be 8
        uint8[] memory numFacetSelectors = new uint8[](selectorCount);
        uint256 counter;
        uint256 numFacets;
        do {
            bytes4 selector = ds.selectors[counter];
            address facetAddressForSelector = ds.selectorTofacet[selector]._facetAddress;
            bool isNewFacet = true;
            for(uint256 index; index<numFacets; index++){
                if(facets_[index].facetAddress == facetAddressForSelector){
                    isNewFacet = false;
                    facets_[index].functionSelectors[numFacetSelectors[index]] = selector;
                    numFacetSelectors[index]++;
                }
            }

            if(isNewFacet){
                 facets_[numFacets].facetAddress = facetAddressForSelector;
                 facets_[numFacets].functionSelectors = new bytes4[](selectorCount);
                 facets_[numFacets].functionSelectors[0] = selector;
                 numFacetSelectors[numFacets]++;
                 numFacets++;
            }

            counter++;
        } while(counter<selectorCount);
        for(uint256 i; i<numFacets; i++){
           bytes4[] memory selectors = facets_[i].functionSelectors;
           uint256 numSelectors = numFacetSelectors[i];
           assembly{
               mstore(selectors, numSelectors)
           }
        }  
        assembly{
               mstore(facets_, numFacets)
        }
    }

    /// @notice Gets all the function selectors supported by a specific facet.
    /// @param _facet The facet address.
    /// @return facetFunctionSelectors_
    function facetFunctionSelectors(address _facet) external override view returns (bytes4[] memory facetFunctionSelectors_){
        LibDiamond._DiamondStorage storage ds = LibDiamond.getDiamondStorage();
        facetFunctionSelectors_ = new bytes4[](ds.selectors.length);
        uint256 numSelectors;
        for(uint256 i; i< ds.selectors.length; i++){
            if(ds.selectorTofacet[ds.selectors[i]]._facetAddress == _facet){
                // add the selector and update the counter
                facetFunctionSelectors_[numSelectors] = ds.selectors[i];
                numSelectors++;
            }
        }
        assembly{
            mstore(facetFunctionSelectors_, numSelectors)
        }
    }

    /// @notice Get all the facet addresses used by a diamond.
    /// @return facetAddresses_
    function facetAddresses() external override view returns (address[] memory facetAddresses_){
        LibDiamond._DiamondStorage storage ds = LibDiamond.getDiamondStorage();
        address[] memory _facetAddresses = new address[](ds.selectors.length);
        uint256 numFacets;
        for(uint256 i; i<ds.selectors.length; i++){
            address factAddress = ds.selectorTofacet[ds.selectors[i]]._facetAddress;
            bool addFacet = true;
            for(uint256 j; j<numFacets; j++){
                if(_facetAddresses[j] == factAddress){
                  addFacet=false;
                }
            }
            if(addFacet){
                _facetAddresses[numFacets] = factAddress;
                numFacets++;
            }
        }
        assembly{
            mstore(_facetAddresses, numFacets)
        }
        return _facetAddresses;
    }

    /// @notice Gets the facet that supports the given selector.
    /// @dev If facet is not found return address(0).
    /// @param _functionSelector The function selector.
    /// @return facetAddress_ The facet address.
    function facetAddress(bytes4 _functionSelector) external override view returns (address facetAddress_){
        LibDiamond._DiamondStorage storage ds = LibDiamond.getDiamondStorage();
        facetAddress_ = ds.selectorTofacet[_functionSelector]._facetAddress;
    }
}