// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title EvidenceProvenance
 * @notice CyberMIND immutable cybersecurity evidence hash registry.
 * @dev Stores ONLY SHA-256 hashes, investigation IDs, and timestamps.
 * Zero sensitive data, PII, or raw logs are stored on-chain.
 */
contract EvidenceProvenance {
    struct EvidenceRecord {
        bytes32 evidenceHash;
        string evidenceId;
        string investigationId;
        uint256 timestamp;
        address anchoredBy;
        string eventType;
    }

    // Mapping from evidenceId => EvidenceRecord
    mapping(string => EvidenceRecord) public records;

    // Events
    event EvidenceAnchored(
        string indexed evidenceId,
        bytes32 indexed evidenceHash,
        string investigationId,
        uint256 timestamp,
        address indexed anchoredBy,
        string eventType
    );

    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only authorized operator can anchor evidence");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @notice Anchor a cryptographic SHA-256 hash of evidence artifact.
     * @param _evidenceId UUID identifier of evidence artifact
     * @param _evidenceHash SHA-256 hash in bytes32 format
     * @param _investigationId Case/Investigation identifier
     * @param _eventType Type of lifecycle event (e.g., CREATED, TRANSFERRED, REVIEWED)
     */
    function anchorEvidence(
        string calldata _evidenceId,
        bytes32 _evidenceHash,
        string calldata _investigationId,
        string calldata _eventType
    ) external {
        require(records[_evidenceId].timestamp == 0, "Evidence hash already anchored");

        records[_evidenceId] = EvidenceRecord({
            evidenceHash: _evidenceHash,
            evidenceId: _evidenceId,
            investigationId: _investigationId,
            timestamp: block.timestamp,
            anchoredBy: msg.sender,
            eventType: _eventType
        });

        emit EvidenceAnchored(
            _evidenceId,
            _evidenceHash,
            _investigationId,
            block.timestamp,
            msg.sender,
            _eventType
        );
    }

    /**
     * @notice Verify whether a provided SHA-256 hash matches the on-chain anchor.
     * @param _evidenceId UUID identifier of evidence artifact
     * @param _candidateHash Candidate SHA-256 hash to compare
     * @return isValid True if identical, false if tampered or mismatched
     */
    function verifyIntegrity(
        string calldata _evidenceId,
        bytes32 _candidateHash
    ) external view returns (bool isValid, uint256 anchoredTimestamp) {
        EvidenceRecord memory record = records[_evidenceId];
        require(record.timestamp > 0, "Evidence record not found");
        return (record.evidenceHash == _candidateHash, record.timestamp);
    }
}
