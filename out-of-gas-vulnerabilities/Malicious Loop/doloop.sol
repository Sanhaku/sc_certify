pragma solidity ^0.8.0;

contract MaliciousLoop {
    uint public count;
    
    function doLoop() public {
        while (true) {
            count++;
        }
    }
}
//doLoop` 函数会一直循环执行，因为 `while (true)` 永远为真。每次循环，`count` 的值都会加 1。由于这个循环永远不会结束，因此该合约的 gas 消耗会不断增加，直到达到 gas 限制。