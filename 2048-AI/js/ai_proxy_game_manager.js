'use strict';

/**
 * This moudule implements a proxy for the game engine (a.k.a the class GameManager)
 * It allows to intercept and/or make calls to the GameManager functions without
 * touching the original source code. If required, it's internal functions can
 * also be redefined.
 *
 * It creates connection with the backend AI Server using the AICommSystem module.
 *
 * To use this class, application.js should substitute GameManager with AIProxyGameManager
 * class to initialize the game.
 */

function AIProxyGameManager(size, InputManager, Actuator, StorageManager) {
    this.aiCommSystem     = new AICommSystem;
    this.aiActionHandlers = new AIActionHanders;

    GameManager.call(this, size, InputManager, Actuator, StorageManager);
}

AIProxyGameManager.prototype = Object.create(GameManager.prototype);

////////////////////////////////////////////////////////////////////////////////////////////////

// Restart the game
/*AIProxyGameManager.prototype.restart = function () {

};*/

// Keep playing after winning (allows going over 2048)
/*AIProxyGameManager.prototype.keepPlaying = function () {

};*/

// Return true if the game is lost, or has won and the user hasn't kept playing
/*AIProxyGameManager.prototype.isGameTerminated = function () {

};*/

// Set up the game
AIProxyGameManager.prototype.setup = function () {
    console.log('Setting up the game...');
    this.aiCommSystem.game.registerNewMoveAction(this.aiActionHandlers.moveTiles);
    GameManager.prototype.setup.call(this);
    this.aiCommSystem.game.requestNextMove();
    console.log('Setup complete...');
};

// Move tiles on the grid in the specified direction
AIProxyGameManager.prototype.move = function (direction) {
    GameManager.prototype.move.call(this, direction);

    // TODO: There should not be an if block! Either the game state should be sent always
    // or it should be sent on demnad. This is done now because the AI is dumb.
    // Moreover movesAvailable() internally calls tileMatchesAvailable() which is an expensive check
    if (this.movesAvailable())
        this.aiCommSystem.game.updateGameState(this.serialize());
};

/*AIProxyGameManager.prototype.findFarthestPosition = function (cell, vector) {

};*/

/*AIProxyGameManager.prototype.movesAvailable = function () {

};*/

// Check for available matches between tiles (more expensive check)
/*AIProxyGameManager.prototype.tileMatchesAvailable = function () {

};*/

/*AIProxyGameManager.prototype.positionsEqual = function (first, second) {

};*/