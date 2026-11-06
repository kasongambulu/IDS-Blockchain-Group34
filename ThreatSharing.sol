// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ThreatSharing {
    
    // Structure pour représenter un indicateur de menace
    struct ThreatIndicator {
        address reporter;       // Adresse de l'organisation/nœud émetteur
        string ipfsHash;        // Lien CID IPFS contenant le détail STIX complet
        string threatType;      // Type d'attaque détecté (ex: FTP-Patator, SSH-Patator)
        uint256 timestamp;      // Date et heure de l'enregistrement
        uint256 severityScore;  // Score de risque ou de sévérité
    }

    // Mapping pour stocker les indicateurs par ID
    mapping(uint256 => ThreatIndicator) public indicators;
    uint256 public indicatorCount;

    // Événement émis lors du partage d'une menace
    event IndicatorShared(
        uint256 indexed id,
        address indexed reporter,
        string ipfsHash,
        string threatType
    );

    /**
     * @dev Enregistre un nouvel indicateur de menace sur la blockchain
     */
    function shareThreat(
        string memory _ipfsHash, 
        string memory _threatType, 
        uint256 _severityScore
    ) public {
        indicators[indicatorCount] = ThreatIndicator({
            reporter: msg.sender,
            ipfsHash: _ipfsHash,
            threatType: _threatType,
            timestamp: block.timestamp,
            severityScore: _severityScore
        });

        emit IndicatorShared(indicatorCount, msg.sender, _ipfsHash, _threatType);
        indicatorCount++;
    }

    /**
     * @dev Récupère les détails d'un indicateur de menace par son ID
     */
    function getIndicator(uint256 _id) public view returns (
        address reporter, 
        string memory ipfsHash, 
        string memory threatType, 
        uint256 timestamp, 
        uint256 severityScore
    ) {
        require(_id < indicatorCount, "Indicateur inexistant.");
        ThreatIndicator memory ind = indicators[_id];
        return (ind.reporter, ind.ipfsHash, ind.threatType, ind.timestamp, ind.severityScore);
    }
}