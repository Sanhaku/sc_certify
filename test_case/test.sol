pragma solidity ^0.5.0;

contract Test {
    address[] internal group;
    mapping(address => bool) internal exists;
    uint256 internal constant MAX_GROUP_SIZE = 50;

    function addMember(address newAddress) public {
        require(!exists[newAddress], "address exists");
        require(group.length < MAX_GROUP_SIZE, "max group size");

        exists[newAddress] = true;
        group.push(newAddress);
    }

    function removeMember(address member) public {
        require(exists[member], "not alerter");
        delete exists[member];
        
        for (uint256 i = 0; i < group.length; ++i) {
            if (group[i] == member) {
                group[i] = group[group.length - 1];
                group.pop();
                break;
            }
        }
    }

    function deleteArray() public {
        delete group;
    }

    function resetLength() public {
        group.length = 0;
    }

    function newArray() public {
        group = new address[](0);
    }

}