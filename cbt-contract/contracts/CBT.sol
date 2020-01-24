pragma solidity ^0.5.0;

contract cbt{
    uint public user_count = 0;

    struct Test{
        uint sn;
        string name;
        string id;
        uint test_datetime;
        uint test_score;
    }

    mapping(uint => Test) public tests;

    constructor() public {
        createTest("suraj jha", "2347h2fj23467", 123);
    }


    function createTest(string memory _name, string memory _id, uint _test_score) public{
        user_count++;
        uint datetime_now = block.timestamp;
        tests[user_count] = Test(user_count, _name, _id, datetime_now, _test_score);
    }
}