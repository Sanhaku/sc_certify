pragma solidity ^0.8.0;

contract MaliciousRecursion {
    uint public count;
    
    function doRecursive(uint x) public {
        if (x > 0) {
            count++;
            doRecursive(x - 1);
        }
    }
}