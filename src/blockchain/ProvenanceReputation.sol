// src/blockchain/ProvenanceReputation.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ProvenanceReputation {
    struct Entry {
        string ipfsHash;
        uint256 timestamp;
        address submitter;
        uint256 reputation;
    }

    Entry[] public entries;
    mapping(bytes32 => uint256) public ipfsToEntry; // store index+1 to avoid zero ambiguity

    event EntryAdded(uint256 indexed idx, string ipfsHash, address submitter, uint256 reputation);

    function addEntry(string memory ipfsHash, uint256 reputation) public {
    bytes32 h = keccak256(abi.encodePacked(ipfsHash));
    require(ipfsToEntry[h] == 0, "already added");

    entries.push(
        Entry({
            ipfsHash: ipfsHash,
            timestamp: block.timestamp,
            submitter: msg.sender,
            reputation: reputation
        })
    );

    ipfsToEntry[h] = entries.length; // store index+1 to avoid zero ambiguity
    emit EntryAdded(entries.length - 1, ipfsHash, msg.sender, reputation);
}


    function getEntry(uint256 idx) public view returns (string memory, uint256, address, uint256) {
        Entry storage e = entries[idx];
        return (e.ipfsHash, e.timestamp, e.submitter, e.reputation);
    }
}
