from brownie import EternalLogicV1, EternalLogicV2, EternalProxy, EternalLogicLibrary, EternalStorage, Contract, accounts

def deploy_contracts():
    accounts[0].deploy(EternalLogicLibrary)
    storage = EternalStorage.deploy({"from": accounts[0]})
    logicv1 = EternalLogicV1.deploy(storage.address, {"from": accounts[0]})
    proxy = EternalProxy.deploy(storage.address, {"from": accounts[0]})
    proxy.setImplementationAddress(logicv1.address)
    return (proxy, logicv1)

def deploy_new_logic():
    accounts[0].deploy(EternalLogicLibrary)
    storage = EternalStorage.deploy({"from": accounts[0]})
    logicv2 = EternalLogicV2.deploy(storage.address,{"from": accounts[0]})
    proxy = EternalProxy[-1]
    proxy.setImplementationAddress(logicv2.address)
    return (proxy, logicv2)

def test_proxy_pattern_owner_is_correct():
    (proxy, logic) = deploy_contracts()
    assert proxy.getOwnerAddress() == accounts[0]

def test_proxy_pattern_implementation_equals_to_logic_address():
    (proxy, logic) = deploy_contracts()
    assert proxy.getImplementationAddress() == logic.address    

def test_can_set_and_get_val_from_logicv1():
    (proxy, logicv1) = deploy_contracts()
    proxy_logicv1 = Contract.from_abi("EternalLogicV1", proxy.address, logicv1.abi)
    proxy_logicv1.setUserAge(30, {"from": accounts[0]})
    assert proxy_logicv1.getUserAge() == 30

def test_can_set_and_get_names_from_logicv1():
    (proxy, logicv1) = deploy_contracts()
    proxy_logicv1 = Contract.from_abi("EternalLogicV1", proxy.address, logicv1.abi)
    proxy_logicv1.setUserName("Boom", {"from": accounts[0]})
    assert proxy_logicv1.getUserName() == "Boom"

def test_proxy_pattern_implementation_equals_to_new_logic_address():
    (proxy, logicv2) = deploy_new_logic()
    assert proxy.getImplementationAddress() == logicv2.address

def test_can_set_and_get_val_from_logicv2():
    (proxy, logicv2) = deploy_new_logic()
    proxy_logicv2 = Contract.from_abi("EternallogicV2", proxy.address, logicv2.abi)
    proxy_logicv2.setUserAge(31, {"from": accounts[0]})
    assert proxy_logicv2.getUserAge() == 31

def test_can_set_and_get_names_from_logicv2():
    (proxy, logicv2) = deploy_contracts()
    proxy_logicv2 = Contract.from_abi("EternalLogicV1", proxy.address, logicv2.abi)
    proxy_logicv2.setUserName("John", {"from": accounts[0]})
    assert proxy_logicv2.getUserName() == "John"
