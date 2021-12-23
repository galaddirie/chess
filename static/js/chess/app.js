//import {Game} from './logic/Game.js'
// import gameConfig from './config/initalGame.js'
// import testGame from './config/testgame.js'
// import {Board} from './ui/Board.js'
import imageConfig from './config/images.js'
var matchId = JSON.parse(document.getElementById('game-id').textContent);


var socket = new WebSocket('ws://'+ window.location.host + '/game/' + matchId + '/')


console.log(socket)

function connect() {
    socket.onopen = function open() {
        console.log('WebSockets connection created.');
        // on websocket open, send the START event.
        socket.send(JSON.stringify({
            "event": "START",
            "message": ""
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
        console.log(data)
        
        // data = data["payload"];
        // let message = data['message'];
        // let event = data["event"];
        // switch (event) {
        //     case "START":
        //         reset();
        //         break;
        //     case "END":
        //         alert(message);
        //         reset();
        //         break;
        //     case "MOVE":
        //         if(message["player"] != char_choice){
        //             make_move(message["index"], message["player"])
        //             myturn = true;
        //             document.getElementById("alert_move").style.display = 'inline';       
        //         }
        //         break;
        //     default:
        //         console.log("No event")
        // }
    };

    if (socket.readyState == WebSocket.OPEN) {
        socket.onopen();
    }
}

//call the connect function at the start.
connect();
function pieceTheme (piece) {
    if (piece in imageConfig){
        return imageConfig[piece]
    }
  }

//C
var config = {
    pieceTheme: pieceTheme,
    draggable: true,
    position: 'start',
}
var board = Chessboard('myBoard', config)
$(window).resize(board.resize)
// var game = document.getElementById('game')
// var board = new Board(gameConfig)
// game.appendChild(board.table);


// var board2 = new Board(testGame)
// game.appendChild(board2.table);




