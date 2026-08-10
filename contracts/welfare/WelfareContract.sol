// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title WelfareContract
 * @dev Contratto per la gestione collettiva di fondi per eventi TAZ
 */
contract WelfareContract {
    address public owner;
    mapping(address => uint256) public shares;
    mapping(address => bool) public crewMembers;
    address[] public crewList;
    
    event PaymentSplit(address indexed recipient, uint256 amount);
    event CrewAdded(address indexed member);
    event CrewRemoved(address indexed member);
    event FundsDeposited(address indexed sender, uint256 amount);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Solo il proprietario");
        _;
    }
    
    /**
     * @dev Aggiunge un membro alla crew
     */
    function addCrew(address member) external onlyOwner {
        require(!crewMembers[member], "Gia' membro");
        crewMembers[member] = true;
        crewList.push(member);
        emit CrewAdded(member);
    }
    
    /**
     * @dev Rimuove un membro dalla crew
     */
    function removeCrew(address member) external onlyOwner {
        require(crewMembers[member], "Non e' membro");
        crewMembers[member] = false;
        emit CrewRemoved(member);
    }
    
    /**
     * @dev Deposita fondi nel contratto
     */
    function deposit() external payable {
        require(msg.value > 0, "Importo deve essere > 0");
        emit FundsDeposited(msg.sender, msg.value);
    }
    
    /**
     * @dev Splitta i fondi tra tutti i membri della crew
     */
    function splitPayment() external onlyOwner {
        uint256 total = address(this).balance;
        require(total > 0, "Nessun fondo da dividere");
        require(crewList.length > 0, "Nessun membro nella crew");
        
        uint256 share = total / crewList.length;
        for (uint i = 0; i < crewList.length; i++) {
            address crew = crewList[i];
            if (crewMembers[crew]) {
                payable(crew).transfer(share);
                emit PaymentSplit(crew, share);
            }
        }
        
        // Rimuovi eventuale resto
        if (address(this).balance > 0) {
            payable(owner).transfer(address(this).balance);
        }
    }
    
    /**
     * @dev Restituisce il numero di membri della crew
     */
    function getCrewCount() external view returns (uint256) {
        return crewList.length;
    }
    
    /**
     * @dev Restituisce l'elenco dei membri della crew
     */
    function getCrewList() external view returns (address[] memory) {
        return crewList;
    }
}
