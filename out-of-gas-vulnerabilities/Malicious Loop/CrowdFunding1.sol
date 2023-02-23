//一个众筹合约，通过迭代数组来支付参与者
pragma solidity ^0.8.0;

contract CrowdFunding2 {
    address[] private contributors;
    mapping(address => uint) public balances;

    function contribute() public payable {
        contributors.push(msg.sender);
        balances[msg.sender] += msg.value;
    }

    function payout() public {
        for (uint i = 0; i < contributors.length; i++) {
            address recipient = contributors[i];
            uint amount = balances[recipient];
            balances[recipient] = 0;
            (bool success, ) = recipient.call{value: amount}("");
            require(success, "Failed to send ether");
        }
    }
}