from brownie import UnstructuredLogicV1, UnstructuredLogicV2, UnstructuredProxy, Contract, accounts

def deploy_contracts():
    logicv1 = UnstructuredLogicV1.deploy({"from": accounts[0]})
    proxy = UnstructuredProxy.deploy({"from": accounts[0]})
    proxy.setImplementationAddress(logicv1.address)
    return (proxy, logicv1)

def deploy_new_logic():
    logicv2 = UnstructuredLogicV2.deploy({"from": accounts[0]})
    proxy = UnstructuredProxy[-1]
    proxy.setImplementationAddress(logicv2.address)
    return (proxy, logicv2)

def test_proxy_pattern_implementation_equals_to_logic_address():
    (proxy, logic) = deploy_contracts()
    assert proxy.getImplementationAddress() == logic.address
    
def test_can_set_and_get_val_from_logicv1():
    (proxy, logicv1) = deploy_contracts()
    proxy_logicv1 = Contract.from_abi("UnstructuredLogicV1", proxy.address, logicv1.abi)
    proxy_logicv1.setVal(10, {"from": accounts[0]})
    assert proxy_logicv1.getVal() == 10

def test_proxy_pattern_implementation_equals_to_new_logic_address():
    (proxy, logicv2) = deploy_new_logic()
    assert proxy.getImplementationAddress() == logicv2.address

def test_can_set_and_get_names_from_logicv2():
    (proxy, logicv2) = deploy_new_logic()
    proxy_logicv2 = Contract.from_abi("UnstructuredLogicV2", proxy.address, logicv2.abi)
    proxy_logicv2.setVal(20, {"from": accounts[0]})
    assert proxy_logicv2.getVal() == 20

