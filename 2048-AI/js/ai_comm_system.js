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
 */

const AI_SERVER_ADDRESS = 'http://localhost:8080';

const AI_ACTION_KEYS = {
    // AI provides a direction to move the tiles
    // Format of data object {key: 'my_move', choice: <direction>}
    // possible values for direction: 'UP', 'RIGHT', 'DOWN', 'LEFT'
    MY_MOVE: 'game_my_move'
}

/////////////////////////////////////////////////////////////////////////////////////////////

function AICommSystem() {
    const self = this;

    self._aiActionHandlers = new AIActionHanders;

    // setup the socket channel on which the AI will play the game
    // also register a listener for messages sent by the AI
    const gameSocket = self._setupChannel.call(self, 'game');
    self._prepareGameActions.call(self, gameSocket);

    return {
        isReady: () => Boolean(gameSocket),

        game: {
            requestNextMove: (state) => self.requestNextMove.call(self, gameSocket, state),
            updateGameState: (state) => self.updateGameState.call(self, gameSocket, state)
        }
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Sends request to play the next move
 */
AICommSystem.prototype.requestNextMove = function(socket, state) {
    console.log('Requesting AI for next move...');
    socket.emit('message', {key: 'play', state});
}

/**
 * Send's the serialization of current game state to the AI server
 */
AICommSystem.prototype.updateGameState = function(socket, state) {
    console.log('Updating AI with game state...');
    socket.emit('message', {key: 'state', state});
}

/////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Configure's the actions to be performed when the AI sends a message
 * to the 'game' namespace
 */
AICommSystem.prototype._prepareGameActions = function(socket) {
    const self = this;

    socket.on('message', (data) => {
        console.log(`Recieved game data: ${JSON.stringify(data)}`);
        if (data.key === AI_ACTION_KEYS.MY_MOVE) {
            self._aiActionHandlers.moveTiles(data);
        }
    });
}

/**
 * Setup socket communication between AI server and the game
 */
AICommSystem.prototype._setupChannel = function(namespace) {
    console.log(`Connecting to AI server as ${namespace}...`);
    const socket = io(`${AI_SERVER_ADDRESS}/${namespace}`);
    console.log('Connected successfully...');
    return socket;
}