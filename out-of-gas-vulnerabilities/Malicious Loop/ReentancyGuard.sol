pragma solidity 0.8.6;

contract ReentancyGuard {
    uint256 public totallent;
    uint256 public taskCount;
    mapping(uint256 => Task) internal tasks;

    struct Task {
        uint256 cost;
    }

    function lendToProject(uint256 cost) external {
        require(cost > 0, "Project: invalid value");
        uint256 newTotallent = totallent + cost;
        require(projectCost() > newTotallent, "Project: value > required");
        totallent = newTotallent;
    }
//在 projectCost 函数中，使用了一个 for 循环来遍历所有任务并计算总成本。如果任务数量很大，则此循环可能需要花费大量的gas，并导致交易超出区块的gas限制，从而被回滚。
    function projectCost() public view returns (uint256 cost) {
        uint256 length = taskCount;
        for (uint256 taskID = 1; taskID <= length; taskID++) {
            cost += tasks[taskID].cost;
        }
        return cost;
    }

    function addTask() external {
        uint256 length = taskCount;
        for (uint256 i = 0; i < length; i++) {
            taskCount++;
            tasks[taskCount].cost = 0;
        }
    }
}
