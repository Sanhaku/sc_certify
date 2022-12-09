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

    function removeAlerter(address alerter) public {
        onlyAdmin();
        require(alerters[alerter], "not alerter");
        delete alerters[alerter];

        for (uint256 i = 0; i < alertersGroup.length; ++i) {
            if (alertersGroup[i] == alerter) {
                alertersGroup[i] = alertersGroup[alertersGroup.length - 1];
                alertersGroup.pop();
                break;
            }
        }
    }

    function onlyAdmin() internal view {
        require(msg.sender == admin, "only admin");
    }
}