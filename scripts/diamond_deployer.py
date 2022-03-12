from brownie import DiamondLoupe, ImplementationAge, ImplementationName, LibAge, LibDiamond, LibName, Diamond, accounts, Contract
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
def get_facet(contract):
    return [
        contract.address,
        get_selectors(contract),
        facetCutAction["Add"]
    ]

def deploy_diamond():
    accounts[0].deploy(LibDiamond)
    diamondContract = Diamond.deploy({"from": accounts[0]})
    return (diamondContract)

def deploy_facets():
    accounts[0].deploy(LibAge)
    accounts[0].deploy(LibName)
    diamondLoupeFacet = DiamondLoupe.deploy({"from": accounts[0]})
    implementationName = ImplementationName.deploy({"from": accounts[0]})
    implementationAge = ImplementationAge.deploy({"from": accounts[0]})
    return (diamondLoupeFacet, implementationName, implementationAge)

def add_facets_to_diamond():
    diamond = Diamond[-1]
    diamondLoupe = DiamondLoupe[-1]
    implementationName = ImplementationName[-1]
    implementationAge = ImplementationAge[-1]
    ## get the selectors and add the selectors for each of them

    diamondLoupeFacet = get_facet(diamondLoupe)
    implementationNameInitializer = get_initiaizer(implementationName)
    implementationNameFacet = get_facet(implementationName)
    implementationAgeInitializer = get_initiaizer(implementationAge)
    implementationAgeFacet = get_facet(implementationAge)   

    tx1=diamond.diamondCut(diamondLoupeFacet, b'', zeroAddress, {"from": accounts[0]})
    tx1.wait(1)

    tx2=diamond.diamondCut(implementationAgeFacet, implementationAgeInitializer, implementationAge.address, {"from": accounts[0]})
    tx2.wait(1)

    tx3=diamond.diamondCut(implementationNameFacet, implementationNameInitializer, implementationName.address, {"from": accounts[0]})
    tx3.wait(1)

    ## Execute all methods with diamond as a proxy - facetAddresses
    diamond_proxy = Contract.from_abi("DiamondLoupe", diamond.address, diamondLoupe.abi)
    
    ## test_facet_addresses
    facetAddresses = diamond_proxy.facetAddresses()
    print("All Facet addresses ", facetAddresses)

    ## Execute all methods with diamond as a proxy - facetFunctionSelectors
    diamondLoupeFunctionSelectors = diamond_proxy.facetFunctionSelectors(diamondLoupe.address)
    implementationNameFunctionSelectors = diamond_proxy.facetFunctionSelectors(implementationName.address)
    implementationAgeFunctionSelectors = diamond_proxy.facetFunctionSelectors(implementationAge.address)

    print("diamondLoupeFunctionSelectors ", diamondLoupeFunctionSelectors)
    print("implementationNameFunctionSelectors ", implementationNameFunctionSelectors)
    print("implementationAgeFunctionSelectors ", implementationAgeFunctionSelectors)

    ## get list of all facets and their selectors
    all_facets = diamond_proxy.facets()
    print("all_facets ", all_facets)
    

def main():
    deploy_diamond()
    deploy_facets()
    add_facets_to_diamond()
