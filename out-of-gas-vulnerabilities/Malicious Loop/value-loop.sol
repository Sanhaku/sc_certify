pragma solidity ^0.8.0;

contract Loop {
    uint256[] values;
    uint256 target;
    uint256 index;
    bool found;
    function search(uint256 _target) public {
    	target = _target;
    	index = 0;
    	found = false;
    	while (index < values.length) {
        	if (values[index] == target) {
            	found = true;
            	break;
        	}
       		index++;
   		}
	}
}