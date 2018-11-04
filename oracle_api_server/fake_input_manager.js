'use strict';

module.exports = FakeInputManager;

///////////////////////////////////////////////////////////////////////////////////

function FakeInputManager() {
    return {
        on: _noop
    }
}

function _noop() {}