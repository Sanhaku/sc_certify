pragma solidity ^0.8.0;

contract Recursive2 {
    uint public count;
    
    function update(uint n) public {
        if (n == 0) {
            count += 1;
        } else {
            update(n-1);
            count += 1;
        }
    }
}