pragma solidity ^0.4.26;

contract ImplicitLoop {
    
    uint256 private b;
    uint256[] private a;

    function add(uint256 c) public {
        a.push(c);
    }

    function loopNormal() public {
        for(uint256 i = 0; i < a.length; i++) {
            a[i] = 0;
        }
    }

    function loopDelete() public {
        delete a;
    }

    function loopLength() public {
        a.length = 0;
    }

    function loopNew() public {
        a = new uint256[](3);
    }
}