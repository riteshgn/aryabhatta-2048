'use strict';

module.exports = FakeActuator;

///////////////////////////////////////////////////////////////////////////////////

function FakeActuator() {
    return {
        actuate: _noop,
        continueGame: _noop
    }
}

function _noop() {}