pragma solidity ^0.8.0;

contract RecursiveCall {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function callme() public {
        require(msg.sender == owner, "Unauthorized");
        this.callme();
    }
}