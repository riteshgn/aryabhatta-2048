// Wait till the browser is ready to render the game (avoids glitches)
window.requestAnimationFrame(function () {
  new AIProxyGameManager(4, KeyboardInputManager, HTMLActuator, LocalStorageManager);
});