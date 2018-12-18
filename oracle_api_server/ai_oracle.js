const GameManager = require('./game_manager');
const FakeInputManager = require('./fake_input_manager');
const FakeActuator = require('./fake_actuator');
const LocalStorageManager = require('./local_storage_manager');
const AIUtils = require('./ai_utils');

const MOVE_CHOICES = {
    UP: 0,
    RIGHT: 1,
    DOWN: 2,
    LEFT: 3
}

const oracle = new Oracle();

module.exports = oracle;

///////////////////////////////////////////////////////////////////////////////////

function Oracle() {
    const self = this;

    self.gm = new GameManager(4, FakeInputManager, FakeActuator, LocalStorageManager);

    return {
        emptyCells: (state) => {
            self.gm.setState(state);
            return self.gm.grid.availableCells();
        },

        availableMoves: (aState) => {
            return Object.keys(MOVE_CHOICES).map(action => {
                const {available, state} = _canMove(self.gm, aState, action);
                return {action, available, state}
            });
        },

        play: (state, choice) => _move(self.gm, state, choice)
    }
}

///////////////////////////////////////////////////////////////////////////////////

function _canMove(gm, state, choice) {
    const newState = _move(gm, state, choice);
    return {available: !_hasSameGridLayout(state, newState), state: newState};
}

function _hasSameGridLayout(state1, state2) {
    const grid1 = state1.grid.cells;
    const grid2 = state2.grid.cells;
    for (let i=0; i<grid1[0].length; i++) {
        for (let j=0; j<grid1.length; j++) {
            if (grid1[i][j] === null && grid2[i][j] !== null) {
                return false;
            }

            if (grid1[i][j] !== null && grid2[i][j] === null) {
                return false;
            }

            if (grid1[i][j] !== null
                && grid2[i][j] !== null
                && grid1[i][j].value !== grid2[i][j].value) {
                return false;
            }
        }
    }

    return true;
}

function _move(gm, state, choice) {
    gm.setState(state);
    // console.log(`==> before`);
    // AIUtils.printGrid(gm.serialize().grid.cells);

    gm.move(MOVE_CHOICES[choice], false);
    // console.log(`==> after (direction: ${choice})`);
    // AIUtils.printGrid(gm.serialize().grid.cells);

    return gm.serialize();
}