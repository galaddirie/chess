//import {Game} from './logic/Game.js'
import gameConfig from './config/initalGame.js'
import testGame from './config/testgame.js'
import {Board} from './ui/Board.js'

var game = document.getElementById('game')
var board = new Board(gameConfig)
game.appendChild(board.table);


// var board2 = new Board(testGame)
// game.appendChild(board2.table);




