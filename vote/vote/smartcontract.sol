// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.0;

contract Voting {
    mapping (address => bool) public hasVoted;
    mapping (string => uint) public votes;

    function vote(string memory option) public {
        require(!hasVoted[msg.sender], "You have already voted");
        hasVoted[msg.sender] = true;
        votes[option] += 1;
    }

    function hasVotedStatus(address voter) public view returns (bool) {
        return hasVoted[voter];
    }
}

// pragma solidity ^0.8.0;

// contract Voting {
//   mapping (address => bool) public hasVoted;
//   mapping (string => uint) public votes;
//   function vote(string memory option) public {
//     require(!hasVoted[msg.sender], "You have already voted");
//     hasVoted[msg.sender] = true;
//     votes[option] += 1;
//   }
// }