// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WelfareContract {
    address public owner;
    mapping(address => uint256) public shares;
    
    constructor() {
        owner = msg.sender;
    }
    
    function distribute(address[] memory recipients) public payable {
        require(msg.sender == owner, "Solo owner");
        uint256 share = msg.value / recipients.length;
        for (uint i = 0; i < recipients.length; i++) {
            shares[recipients[i]] += share;
        }
    }
}
