//import {Game} from './logic/Game.js'
// import gameConfig from './config/initalGame.js'
// import testGame from './config/testgame.js'
// import {Board} from './ui/Board.js'
import imageConfig from './config/images.js'
var matchId = JSON.parse(document.getElementById('game-id').textContent);


var socket = new WebSocket('ws://'+ window.location.host + '/game/' + matchId + '/')


console.log(socket)
var board = null
var game = null
const options = {'imagesPath':'../../static/vendor/AbChess/images/wiki/'}

var movesCount = 0;
var abChess = new AbChess("chessboard", options);


abChess.onMovePlayed(
    function(){
        socket.send(JSON.stringify({
            'event': 'MOVE',
            'message':{'fen': abChess.getFEN(movesCount+1)},
        }))
    }
    
)


function connect() {
    socket.onopen = function open() {
        console.log('WebSockets connection created.');
        // on websocket open, send the START event.
        socket.send(JSON.stringify({
            "event": "START",
            "message": {'fen':''}
        }));
    };

    socket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };
    // Sending the info about the room
    socket.onmessage = function (e) {
        // On getting the message from the server
        // Do the appropriate steps on each event.
        let data = JSON.parse(e.data);
        
        data = data["payload"];
        let message = data['content'];
        let event = data["event"];
        console.log(message)
        switch (event) {
            case "START":
                abChess.setFEN(message['fen']);
                break;
            case "END":
                alert(message);
                
                break;
            case "MOVE":
                movesCount +=1
                abChess.setFEN(message['fen'])
                
                // board.position(message['fen'])
                break;
            default:
                console.log("No event")
        }
    };

    if (socket.readyState == WebSocket.OPEN) {
        socket.onopen();
    }
}

//call the connect function at the start.
connect();


// var game = document.getElementById('game')
// var board = new Board(gameConfig)
// game.appendChild(board.table);


// var board2 = new Board(testGame)
// game.appendChild(board2.table);




