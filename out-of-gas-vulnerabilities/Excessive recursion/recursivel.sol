pragma solidity ^0.8.0;

contract Recursive1 {
    function recursiveCall() public {
        recursiveCall();
    }
}