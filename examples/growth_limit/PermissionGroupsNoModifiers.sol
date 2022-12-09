pragma solidity 0.6.6;

contract PermissionGroupsNoModifiers {
    address public admin;
    mapping(address => bool) internal alerters;
    address[] internal alertersGroup;
    uint256 internal constant MAX_GROUP_SIZE = 50;

    constructor(address _admin) public {
        require(_admin != address(0), "admin 0");
        admin = _admin;
    }

    function addAlerter(address newAlerter) public {
        onlyAdmin();
        require(!alerters[newAlerter], "alerter exists"); // prevent duplicates.
        require(alertersGroup.length < MAX_GROUP_SIZE, "max alerters");

        alerters[newAlerter] = true;
        alertersGroup.push(newAlerter);
    }

    function onlyAdmin() internal view {
        require(msg.sender == admin, "only admin");
    }
}