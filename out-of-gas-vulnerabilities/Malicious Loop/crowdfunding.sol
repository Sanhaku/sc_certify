pragma solidity ^0.4.24;

contract Crowdfunding1 {
    address[] private supporters;
    mapping (address => uint) public contributions;

    function contribute() payable public {
        supporters.push(msg.sender);
        contributions[msg.sender] += msg.value;
    }

    function payoutAll() public {
        for(uint i = 0; i < supporters.length; i++) {
         
            require(supporters[i].send(contributions[supporters[i]]));
            contributions[supporters[i]] = 0;
        }
        delete supporters; // Remove all supporters after payout
    }
}
//在`payout()`函数中，合约尝试从`contributors`数组中遍历每个地址，以将其余额发送到对应地址。但如果`contributors`数组长度很大，遍历整个数组的过程将消耗大量的 gas