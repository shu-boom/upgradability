from brownie import LogicV1, LogicV2, Proxy, CommonStorage, Contract, accounts

def deploy_contracts():
    logicv1 = LogicV1.deploy({"from": accounts[0]})
    proxy = Proxy.deploy({"from": accounts[0]})
    proxy.upgradeTo(logicv1.address)
    return (proxy, logicv1)

def deploy_new_logic():
    logicv2 = LogicV2.deploy({"from": accounts[0]})
    proxy = Proxy[-1]
    proxy.upgradeTo(logicv2.address)
    return (proxy, logicv2)

def test_proxy_pattern_implementation_equals_to_logic_address():
    (proxy, logic) = deploy_contracts()
    assert proxy.getImplementationAddress() == logic.address
    
def test_can_set_and_get_names_from_logicv1():
    (proxy, logicv1) = deploy_contracts()
    proxy_logicv1 = Contract.from_abi("LogicV1", proxy.address, logicv1.abi)
    proxy_logicv1.setFirstName("John", {"from": accounts[0]})
    proxy_logicv1.setLastName("Doe", {"from": accounts[0]})
    assert proxy_logicv1.getFirstName() == "John"
    assert proxy_logicv1.getLastName() == "Doe"

def test_can_set_value_from_proxy():
    (proxy, logicv2) = deploy_new_logic()
    assert proxy.getImplementationAddress() == logicv2.address

def test_can_set_and_get_names_from_logicv2():
    (proxy, logicv2) = deploy_contracts()
    proxy_logicv2 = Contract.from_abi("LogicV2", proxy.address, logicv2.abi)
    proxy_logicv2.setFirstName("Paul", {"from": accounts[0]})
    proxy_logicv2.setLastName("Walker", {"from": accounts[0]})
    assert proxy_logicv2.getFirstName() == "Paul"
    assert proxy_logicv2.getLastName() == "Walker"

def test_can_get_and_set_age_from_proxy():
    (proxy, logicv2) = deploy_new_logic()
    proxy_logicv2 = Contract.from_abi("LogicV2", proxy.address, logicv2.abi)
    proxy_logicv2.setAge(10, {"from": accounts[0]})
    assert proxy_logicv2.getAge() == 10
