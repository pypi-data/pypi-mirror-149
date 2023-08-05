pragma solidity >=0.8.0 <0.9.0;


contract BasicContract {
    uint256 public state;

    constructor(uint256 _state) {
        state = _state;
    }

    function setState(uint256 _x) public {
        state = _x;
    }

    function payableSetState(uint256 _x) public payable {
        state = _x;
    }

    function faultySetState(uint256 _x) public {
        if (_x == 0) {
            revert("Wrong value");
        }
        state = _x;
    }

    function getState(uint256 _x) public view returns (uint256) {
        return state + _x;
    }
}


contract ConstructionError {
    constructor(uint256 _x) {
        if (_x == 0) {
            revert("Wrong value");
        }
    }
}


contract TransactionError {
    function setState(uint256 _x) public {
        if (_x == 0) {
            revert("Wrong value");
        }
    }
}


contract PayableConstructor {
    uint256 public state;

    constructor(uint256 _state) payable {
        state = _state;
    }
}
