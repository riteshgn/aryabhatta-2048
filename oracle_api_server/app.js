'use strict';

const restify = require('restify');

const GameManager = require('./game_manager');
const FakeInputManager = require('./fake_input_manager');
const FakeActuator = require('./fake_actuator');
const LocalStorageManager = require('./local_storage_manager');

const MOVE_CHOICES = {
    UP: 0,
    RIGHT: 1,
    DOWN: 2,
    LEFT: 3
}


const gm = new GameManager(4, FakeInputManager, FakeActuator, LocalStorageManager);

const server = restify.createServer();
server.use(restify.plugins.bodyParser());
server.post('/oracle/play', play);
server.post('/oracle/available_cells', availableCells);

server.listen(18080, function() {
    console.log('%s listening at %s', server.name, server.url);
});


///////////////////////////////////////////////////////////////////////////////////

function availableCells(req, res, next) {
    gm.setState(req.body.state);
    res.send(200, gm.grid.availableCells());
    next();
}

function play(req, res, next) {
    gm.setState(req.body.state);
    // console.log(`==> before`);
    // printGrid(gm.serialize().grid.cells);

    gm.move(MOVE_CHOICES[req.body.choice], false);
    // console.log(`==> after (direction: ${req.body.choice})`);
    // printGrid(gm.serialize().grid.cells);

    res.send(200, {state: gm.serialize()});
    next();
}

///////////////////////////////////////////////////////////////////////////////////

function printGrid(grid, digitsInMaxScore=4) {
    const gridTranspose = _transpose(grid);
    const gridToPrint = _printableGrid(gridTranspose, digitsInMaxScore);
    const border = _printableBorder(digitsInMaxScore);
    const cell_separator = '|';

    console.log('');
    console.log(border);
    gridToPrint.forEach(row => {
        console.log(`${cell_separator}${row}${cell_separator}`);
        console.log(border);
    });
    console.log('');
}

///////////////////////////////////////////////////////////////////////////////////

function _transpose(arr) {
    const arrTranspose = []
    for(let i=0; i<arr[0].length; i++) {
        const innerArr = [];
        for(let j=0; j<arr.length; j++) {
            innerArr.push(arr[j][i]);
        }
        arrTranspose.push(innerArr);
    }
    return arrTranspose;
}

function _printableGrid(grid, digitsInMaxScore) {
    const totalCharsWithSpacing = digitsInMaxScore + 2;
    return grid.map(row => {
        const printableCells = row.map(cell => {
            let cellValue = Array(totalCharsWithSpacing).fill(' ').join('');

            if (cell) {
                const zeros = Array(digitsInMaxScore).fill(0).join('');
                cellValue = ` ${(zeros + cell.value).slice(-1 * digitsInMaxScore)} `;
            }

            return cellValue;
        });

        return printableCells.join('|');
    });
}

function _printableBorder(digitsInMaxScore) {
    const totalCharsWithSpacing = digitsInMaxScore + 2;
    const dashes = Array(digitsInMaxScore).fill(
        Array(totalCharsWithSpacing).fill('-').join('')
    ).join(' ');
    return ` ${dashes} `;
}