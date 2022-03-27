from brownie import Implementation1, Implementation2, MetamorphicFactory,  accounts, Contract
import brownie
from web3 import Web3
# Create an object from the WEB3 lib
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
from brownie.convert import to_bytes

## bytecode copied from remix. The bytecode returned by Brownie is not complete. Need to check the reason for it. 
BYTECODE_IMPLEMENTATION1 = '0x608060405234801561001057600080fd5b5061017b806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c806309efb8ff146100465780632b68b9c614610064578063ac5886751461006e575b600080fd5b61004e61008a565b60405161005b9190610104565b60405180910390f35b61006c610090565b005b610088600480360381019061008391906100c8565b6100a9565b005b60005481565b3373ffffffffffffffffffffffffffffffffffffffff16ff5b8060008190555050565b6000813590506100c28161012e565b92915050565b6000602082840312156100de576100dd610129565b5b60006100ec848285016100b3565b91505092915050565b6100fe8161011f565b82525050565b600060208201905061011960008301846100f5565b92915050565b6000819050919050565b600080fd5b6101378161011f565b811461014257600080fd5b5056fea26469706673582212200286695eceafc3248eb70914bd154ea05f3323acc9c53853095d8234043ccbe064736f6c63430008070033'
BYTECODE_IMPLEMENTATION2 = '0x608060405234801561001057600080fd5b5061020f806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c806309efb8ff146100465780632b68b9c614610064578063ac5886751461006e575b600080fd5b61004e61008a565b60405161005b919061010f565b60405180910390f35b61006c610090565b005b610088600480360381019061008391906100d3565b6100a9565b005b60005481565b3373ffffffffffffffffffffffffffffffffffffffff16ff5b80816100b5919061012a565b60008190555050565b6000813590506100cd816101c2565b92915050565b6000602082840312156100e9576100e86101bd565b5b60006100f7848285016100be565b91505092915050565b61010981610184565b82525050565b60006020820190506101246000830184610100565b92915050565b600061013582610184565b915061014083610184565b9250817fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff04831182151516156101795761017861018e565b5b828202905092915050565b6000819050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600080fd5b6101cb81610184565b81146101d657600080fd5b5056fea2646970667358221220f2b8624e3944aeeb7a1018289990f4b6e0e42d4aa4fb632d2b9187f887682a0f64736f6c63430008070033'
def deployFactoryContract():
    account = accounts[0]
    return MetamorphicFactory.deploy({"from": account})

def deployImplementation1():
    account = accounts[0]
    return Implementation1.deploy({"from": account})

def deployImplementation2():
    account = accounts[0]
    return Implementation2.deploy({"from": account})

def test_can_set_correct_implmentation_after_deploy():
    account = accounts[0]
    factory_contract = deployFactoryContract()
    implementation_contract = deployImplementation1()
    factory_contract.deploy(b'1', BYTECODE_IMPLEMENTATION1, {"from": account})
    ## Due to nonce the contract address differs due to deployment 2 times. In this test case, we have saved the contract address generated for the first time using Ganache for assertion. My apologies to the programming gods :( 
    assert implementation_contract == "0x602C71e4DAC47a042Ee7f46E0aee17F94A3bA0B6"

def test_can_set_value_using_metamorphic_address():
    account = accounts[0]
    factory_contract = deployFactoryContract()
    implementation1=deployImplementation1()
    tx = factory_contract.deploy(b'1', BYTECODE_IMPLEMENTATION1, {"from": account})
    metamorphicCodeAddress = factory_contract._getMetamorphicContractAddress(b'1', '0x5860208158601c335a63aaf10f428752fa158151803b80938091923cf3')
    assert tx.events["Deployed"][0]["_addr"] == metamorphicCodeAddress
    metamorphic_proxy = Contract.from_abi("Implementation1", metamorphicCodeAddress, implementation1.abi)
    metamorphic_proxy.setInteger(2, {"from": account})
    assert metamorphic_proxy.integer() == 2


def test_implementation_change_and_metamorphic_address_dont_change_after_upgrade():
    account = accounts[0]
    factory_contract = deployFactoryContract()
    implementation1=deployImplementation1()
    metamorphicCodeAddress = factory_contract._getMetamorphicContractAddress(b'1', '0x5860208158601c335a63aaf10f428752fa158151803b80938091923cf3')
    tx = factory_contract.deploy(b'1', BYTECODE_IMPLEMENTATION1, {"from": account})
    assert tx.events["Deployed"][0]["_addr"] == metamorphicCodeAddress
    ## delete the existing contract at that address 
    metamorphic_proxy = Contract.from_abi("Implementation1", metamorphicCodeAddress, implementation1.abi)
    txd = metamorphic_proxy.destruct({"from": account})
    txd.wait(1)
    tx2 = factory_contract.deploy(b'1', BYTECODE_IMPLEMENTATION2, {"from": account})
    assert tx2.events["Deployed"][0]["_addr"] == metamorphicCodeAddress
    metamorphic_proxy.setInteger(2, {"from": account})
    assert metamorphic_proxy.integer() == 4
