from brownie import DiamondLoupe, ImplementationAge, ImplementationName, LibAge, LibDiamond, LibName, Diamond, TestReplace, accounts, Contract
import brownie
import web3

facetCutAction = {"Add": 0, "Replace": 1, "Remove": 2}

zeroAddress = "0x0000000000000000000000000000000000000000"

def get_initiaizer(contract):
    init = '0x'
    if('initialize' in contract.signatures):
        init = contract.signatures.pop('initialize')
    return init

def get_selectors(contract):
    selector_dict = contract.signatures
    selectors = list(selector_dict.values())
    return (selectors)

def hashFunctionSignature(function_signature_text):
    return web3.Web3.keccak(text=function_signature_text).hex()[0:10]

## returns the facet from the contract
def get_facet(contract, action="Add"):
    return [
        contract.address,
        get_selectors(contract),
        facetCutAction[action]
    ]

def deploy_diamond(owner):
    owner.deploy(LibDiamond)
    diamondContract = Diamond.deploy({"from": owner})
    return (diamondContract)

def deploy_facets(owner):
    owner.deploy(LibAge)
    owner.deploy(LibName)
    diamondLoupe = DiamondLoupe.deploy({"from": owner})
    implementationName = ImplementationName.deploy({"from": owner})
    implementationAge = ImplementationAge.deploy({"from": owner})
    return (diamondLoupe, implementationName, implementationAge)

def test_should_provide_all_the_facets_and_their_respective_selectors():
    owner = accounts[0]
    diamond = deploy_diamond(owner)
    (diamondLoupe, implementationName, implementationAge)=deploy_facets(owner)
    implementationAgeInitializer = get_initiaizer(implementationAge)
    implementationNameInitializer = get_initiaizer(implementationName)

    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, diamondLoupe.abi)
    diamond.diamondCut(get_facet(diamondLoupe, "Add"), b'', zeroAddress, {"from": owner})    
    diamond.diamondCut(get_facet(implementationName, "Add"), implementationNameInitializer, implementationName.address, {"from": owner})
    diamond.diamondCut(get_facet(implementationAge, "Add"), implementationAgeInitializer, implementationAge.address, {"from": owner})
    allFacets = diamond_proxy.facets()
    print(allFacets)
    assert(len(allFacets) == 3)
    assert(allFacets[0][0] == diamondLoupe.address)
    assert(allFacets[0][1] == get_selectors(diamondLoupe))

    assert(allFacets[1][0] == implementationName.address)
    assert(allFacets[1][1] == get_selectors(implementationName))

    assert(allFacets[2][0] == implementationAge.address)
    assert(allFacets[2][1] == get_selectors(implementationAge))


def test_should_provide_all_the_facet_addresses():
    owner = accounts[0]
    diamond = deploy_diamond(owner)
    (diamondLoupe, implementationName, implementationAge)=deploy_facets(owner)
    implementationAgeInitializer = get_initiaizer(implementationAge)
    implementationNameInitializer = get_initiaizer(implementationName)

    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, diamondLoupe.abi)
    diamond.diamondCut(get_facet(diamondLoupe, "Add"), b'', zeroAddress, {"from": owner})    
    diamond.diamondCut(get_facet(implementationName, "Add"), implementationNameInitializer, implementationName.address, {"from": owner})
    diamond.diamondCut(get_facet(implementationAge, "Add"), implementationAgeInitializer, implementationAge.address, {"from": owner})
    addresses = diamond_proxy.facetAddresses()
    assert(len(addresses) == 3)
    assert(addresses == [diamondLoupe.address, implementationName.address, implementationAge.address])


def test_should_add_facet_to_diamond():
    owner = accounts[0]
    diamond = deploy_diamond(owner)
    diamondLoupe = DiamondLoupe.deploy({"from": owner})
    diamondLoupeFacet = get_facet(diamondLoupe, "Add")
    tx1=diamond.diamondCut(diamondLoupeFacet, b'', zeroAddress, {"from": owner})
    tx1.wait(1)
    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, diamondLoupe.abi)
    facetAddresses = diamond_proxy.facetAddresses()
    print(facetAddresses)
    assert(len(facetAddresses) == 1)
    diamondLoupeFunctionSelectors = diamond_proxy.facetFunctionSelectors(diamondLoupe.address)
    assert(diamondLoupeFunctionSelectors == get_selectors(diamondLoupe))

def test_should_only_allow_owner_to_manipulate_facets():
    owner = accounts[0]
    maliciousOwner = accounts[1]
    diamond = deploy_diamond(owner)
    diamondLoupe = DiamondLoupe.deploy({"from": owner})
    diamondLoupeFacet = get_facet(diamondLoupe, "Add")
    with brownie.reverts():
        diamond.diamondCut(diamondLoupeFacet, b'', zeroAddress, {"from": maliciousOwner})

def test_should_add_a_selector_from_facet():
    owner = accounts[0]
    diamond = deploy_diamond(owner)
    diamondLoupe = DiamondLoupe.deploy({"from": owner})
    ## get the list of selectors and pop one from the list. Add the last one using the diamond cut later 
    selectors = get_selectors(diamondLoupe)
    extraSelector = [selectors.pop()]
    selectorsFacet = [diamondLoupe.address, selectors, facetCutAction["Add"]]    
    extraSelectorFacet = [diamondLoupe.address, extraSelector, facetCutAction["Add"]]
    

    txToAddSelector=diamond.diamondCut(selectorsFacet, b'', zeroAddress, {"from": owner})
    txToAddSelector.wait(1)
    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, diamondLoupe.abi)
    
    ## check diamond loupe's function response
    diamondLoupeFunctionSelectors = diamond_proxy.facetFunctionSelectors(diamondLoupe.address)
    assert(len(diamondLoupeFunctionSelectors) == len(selectors))
    assert(diamondLoupeFunctionSelectors == selectors)

    txToAddExtraSelector=diamond.diamondCut(extraSelectorFacet, b'', zeroAddress, {"from": owner})
    txToAddExtraSelector.wait(1)
    diamondLoupeFunctionSelectorsWithExtraSelector = diamond_proxy.facetFunctionSelectors(diamondLoupe.address)

    assert(len(diamondLoupeFunctionSelectorsWithExtraSelector) == len(selectors) + len(extraSelector) )
    assert(diamondLoupeFunctionSelectorsWithExtraSelector == selectors+extraSelector)

def test_should_replace_a_selector_from_facet():
    owner = accounts[0]
    diamond = deploy_diamond(owner)
    diamondLoupe = DiamondLoupe.deploy({"from": owner})
    selectors = get_selectors(diamondLoupe)
    selectorsFacet = [diamondLoupe.address, selectors, facetCutAction["Add"]]    
    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, diamondLoupe.abi)
    selectorToReplace = selectors[len(selectors) - 1]
    
    addressToReplaceTo = TestReplace.deploy({"from": owner})
    replacementSelectorFacet = [addressToReplaceTo.address, [selectorToReplace], facetCutAction["Replace"]]

    txToAddSelector=diamond.diamondCut(selectorsFacet, b'', zeroAddress, {"from": owner})
    txToAddSelector.wait(1)
    facetAddress = diamond_proxy.facetAddress(selectorToReplace)
    assert(facetAddress == diamondLoupe.address)

    ## find a selector to replace. This test chooses the last selector. 
    txToReplaceSelectorAddress=diamond.diamondCut(replacementSelectorFacet, b'', zeroAddress, {"from": owner})
    txToReplaceSelectorAddress.wait(1)
    replacedFacetAddress = diamond_proxy.facetAddress(selectorToReplace)
    assert(replacedFacetAddress == addressToReplaceTo)

def test_should_remove_a_selector_from_facet():
    owner = accounts[0]
    diamond = deploy_diamond(owner)
    diamondLoupe = DiamondLoupe.deploy({"from": owner})
    ## get the list of selectors and pop one from the list. Add the last one using the diamond cut later 
    selectors = get_selectors(diamondLoupe)
    selectorsFacet = [diamondLoupe.address, selectors, facetCutAction["Add"]]    
    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, diamondLoupe.abi)

    txToAddSelector=diamond.diamondCut(selectorsFacet, b'', zeroAddress, {"from": owner})
    txToAddSelector.wait(1)
    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, diamondLoupe.abi)
    
    ## check diamond loupe's function response
    diamondLoupeFunctionSelectors = diamond_proxy.facetFunctionSelectors(diamondLoupe.address)
    assert(len(diamondLoupeFunctionSelectors) == len(selectors))
    assert(diamondLoupeFunctionSelectors == selectors)
    
    selectorToRemove = selectors.pop()
    removeSelectorFacet = [diamondLoupe.address, [selectorToRemove], facetCutAction["Remove"]]
    txToRemoveSelector=diamond.diamondCut(removeSelectorFacet, b'', zeroAddress, {"from": owner})
    txToRemoveSelector.wait(1)

    diamondLoupeFunctionSelectorsWithSelectorRemoved = diamond_proxy.facetFunctionSelectors(diamondLoupe.address)
    assert(len(diamondLoupeFunctionSelectorsWithSelectorRemoved) == len(selectors))
    assert(diamondLoupeFunctionSelectorsWithSelectorRemoved == selectors)

def test_should_get_and_set_name_from_implementation():
    owner = accounts[0]
    diamond = deploy_diamond(owner)
    implementationName = ImplementationName.deploy({"from": owner})
    implementationNameInitializer = get_initiaizer(implementationName)
    ImplementationNameFacet = get_facet(implementationName, "Add")
    diamond.diamondCut(ImplementationNameFacet, implementationNameInitializer, implementationName.address, {"from": owner})
    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, ImplementationName.abi)
    newName = "John"
    initialUserName = diamond_proxy.getUserName()
    assert(initialUserName == "Boom")
    diamond_proxy.setUserName(newName, {"from": owner})
    assert(diamond_proxy.getUserName() == newName)

def test_should_get_and_set_age_from_implementation():
    owner = accounts[0]
    diamond = deploy_diamond(owner)
    implementationAge = ImplementationAge.deploy({"from": owner})
    implementationAgeInitializer = get_initiaizer(implementationAge)
    ImplementationAgeFacet = get_facet(implementationAge, "Add")
    diamond.diamondCut(ImplementationAgeFacet, implementationAgeInitializer, implementationAge.address, {"from": owner})
    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, ImplementationAge.abi)
    newAge = 35
    initialUserAge = diamond_proxy.getUserAge()
    assert(initialUserAge == 27)
    diamond_proxy.setUserAge(newAge, {"from": owner})
    assert(diamond_proxy.getUserAge() == newAge)
