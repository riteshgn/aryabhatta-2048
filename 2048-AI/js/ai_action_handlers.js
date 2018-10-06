'use strict';

/**
 * Utility module which parses data sent from the AI server and
 * produces meaningful action(s)
 */

function AIActionHanders() {
    return {
        moveTiles
    }
}

///////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Generates a keydown event in the described direction.
 * Format of input data
 *     {key: 'my_move', choice: <direction>}
 * possible values for direction: 'UP', 'RIGHT', 'DOWN', 'LEFT'
 */
function moveTiles(data) {
    const keyMap = {
        UP: {key: 'ArrowUp', code: 38},
        RIGHT: {key: 'ArrowRight', code: 39},
        DOWN: {key: 'ArrowDown', code: 40},
        LEFT: {key: 'ArrowLeft', code: 37},
    }
    const keyboard = keyMap[data.choice || 'UP'];

    // source: https://elgervanboxtel.nl/site/blog/simulate-keydown-event-with-javascript
    const keyDownEvent = new Event('keydown');
    keyDownEvent.key      = keyboard.key;
    keyDownEvent.keyCode  = keyboard.code;
    keyDownEvent.which    = keyDownEvent.keyCode;
    keyDownEvent.altKey   = false;
    keyDownEvent.ctrlKey  = false;
    keyDownEvent.shiftKey = false;
    keyDownEvent.metaKey  = false;
    document.dispatchEvent(keyDownEvent);
}