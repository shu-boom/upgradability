from brownie import LogicV1, LogicV2, Proxy, CommonStorage, Contract, accounts

def deploy_contracts():
    logic_tx = LogicV1.deploy({"from": accounts[0]})
    proxy_tx = Proxy.deploy({"from": accounts[0]})
    proxy_tx = CommonStorage.deploy({"from": accounts[0]})
    proxy_tx.setImplementationAddress(logic_tx.address)
    return (proxy_tx, logic_tx.address)

# def test_proxy_pattern_implementation_equals_to_logic_address():
#     (proxy, logicAddress) = deploy_contracts()
#     assert proxy.getImplementationAddress() == logicAddress
    
# def test_can_get_value_from_implementation():
#     (proxy, logicAddress) = deploy_contracts()
#     proxy_logic = Contract.from_abi("Logic", proxy.address, Logic.abi)
#     assert proxy_logic.getMyInt() == 10
    
# def test_can_set_value_from_proxy():
#     (proxy, logicAddress) = deploy_contracts()
#     proxy_logic = Contract.from_abi("Logic", proxy.address, Logic.abi)
#     proxy_logic.setMyInt(20, {"from": accounts[0]})
#     assert proxy.getImplementationAddress() == logicAddress