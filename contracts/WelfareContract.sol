// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WelfareContract {
    address public owner;
    uint256 public totalFunds;
    mapping(address => uint256) public shares;
    mapping(address => bool) public crewMembers;
    address[] public crewList;
    
    event PaymentSplit(address indexed recipient, uint256 amount);
    event CrewAdded(address indexed member);
    event CrewRemoved(address indexed member);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Solo il proprietario");
        _;
    }
    
    function addCrew(address member) external onlyOwner {
        require(!crewMembers[member], "Gia' membro");
        crewMembers[member] = true;
        crewList.push(member);
        emit CrewAdded(member);
    }
    
    function removeCrew(address member) external onlyOwner {
        require(crewMembers[member], "Non e' membro");
        crewMembers[member] = false;
        emit CrewRemoved(member);
    }
    
    function deposit() external payable {
        totalFunds += msg.value;
    }
    
    function splitPayment() external onlyOwner {
        uint256 share = totalFunds / crewList.length;
        for (uint i = 0; i < crewList.length; i++) {
            address crew = crewList[i];
            if (crewMembers[crew]) {
                payable(crew).transfer(share);
                emit PaymentSplit(crew, share);
            }
        }
        totalFunds = 0;
    }
}
