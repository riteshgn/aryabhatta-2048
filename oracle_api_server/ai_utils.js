'use strict';

module.exports = {
    printGrid
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