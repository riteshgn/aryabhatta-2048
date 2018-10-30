'use strict';

/**
 * This module provides the communication framework to interact between the game and the AI.
 * The communication is established using the socket-io library.
 *
 * There are 2 ways in which the game's engine is exposed to the AI
 *     1. As the namespace 'game'
 *         Provides below APIs
 *         - requestNextMove() -> will ask the AI to play
 *         - updateGameState(state) -> will send the current game's state to the AI
 *         - registerNewMoveAction(action) -> register the callback function which must be
 *                                            triggered when the AI makes a move
 *
 *     2. As the namespace 'oracle'
 *         Here the game engine will expose the game's core which can be used by the AI
 *         to figure out its next move
 *         - To be implemented -
 */

const AI_SERVER_ADDRESS = 'http://localhost:8080';

const AI_ACTION_KEYS = {
    // AI provides a direction to move the tiles
    // Format of data object {key: 'my_move', choice: <direction>}
    // possible values for direction: 'UP', 'RIGHT', 'DOWN', 'LEFT'
    MY_MOVE: 'my_move'
}

/////////////////////////////////////////////////////////////////////////////////////////////

function AICommSystem() {
    const self = this;

    // stores callbacks for the different actions which can be performed by the AI
    // see AI_ACTION_KEYS for more definitions
    const gameActions = {};

    // setup the socket chnnale on which the AI will play the game
    // also register a listener for messages sent by the AI
    const gameSocket = self.setupChannel.call(self, 'game');
    gameSocket.on('message', (data) => {
        console.log(`Recieved data: ${JSON.stringify(data)}`);
        self.executeAction.call(self, gameActions, data);
    });

    return {
        isReady: () => Boolean(gameSocket),

        game: {
            requestNextMove: (state) => self.requestNextMove.call(self, gameSocket, state),
            updateGameState: (state) => self.updateGameState.call(self, gameSocket, state),
            registerNewMoveAction: (action) => self.registerActions.call(self, gameActions, AI_ACTION_KEYS.MY_MOVE, action)
        }
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Register's an action callback
 */
AICommSystem.prototype.registerActions = function(actions, key, action) {
    if (!actions[key]) {
        actions[key] = [];
    }

    console.log(`Registering action for '${key}'`);
    actions[key].push(action);
}

/**
 * Executes registered callback(s)
 */
AICommSystem.prototype.executeAction = function(actions, data) {
    if (!data.key) {
        console.log('Received data does not have a key. Cannot map to a handler!');
        return;
    }

    if (!actions[data.key]) {
        console.log(`No actions registered for key: ${data.key}!`);
        return;
    }

    actions[data.key].forEach(handle => handle(data));
}

/**
 * Sends request to play the next move
 */
AICommSystem.prototype.requestNextMove = function(socket, state) {
    console.log('Requesting AI for next move...');
    socket.emit('message', {key: 'play', state});
}

/**
 * Setup socket communication between AI server and the game
 */
AICommSystem.prototype.setupChannel = function(namespace) {
    console.log(`Connecting to AI server as ${namespace}...`);
    const socket = io(`${AI_SERVER_ADDRESS}/${namespace}`);
    console.log('Connected successfully...');
    return socket;
}

/**
 * Send's the serialization of current game state to the AI server
 */
AICommSystem.prototype.updateGameState = function(socket, state) {
    console.log('Updating AI with game state...');
    socket.emit('message', {key: 'state', state});
}