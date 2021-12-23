import imageConfig from './config/images.js'
import {INPUT_EVENT_TYPE, Chessboard, COLOR, BORDER_TYPE, MARKER_TYPE} from './../../vendor/cm-chessboard/src/cm-chessboard/Chessboard.js'


var matchId = JSON.parse(document.getElementById('game-id').textContent);
var socket = new WebSocket('ws://'+ window.location.host + '/game/' + matchId + '/')
const chess = new Chess()
const board = new Chessboard(document.getElementById("chessboard"),{
    position: "start", // set as fen, "start" or "empty"
    orientation: COLOR.white, // white on bottom
    style: {
        cssClass: "default",
        showCoordinates: true, // show ranks and files
        borderType: BORDER_TYPE.thin, // thin: thin border, frame: wide border with coordinates in it, none: no border
        aspectRatio: 1, // height/width. Set to `undefined`, if you want to define it only in the css.
        moveFromMarker: MARKER_TYPE.frame, // the marker used to mark the start square
        moveToMarker: MARKER_TYPE.frame // the marker used to mark the square where the figure is moving to
    },
    responsive: true, // resizes the board based on element size
    animationDuration: 300, // pieces animation duration in milliseconds
    sprite: {
        url: "./../../static/vendor/cm-chessboard/assets/images/chessboard-sprite-staunty.svg", // pieces and markers are stored as svg sprite
        size: 40, // the sprite size, defaults to 40x40px
        cache: true // cache the sprite inline, in the HTML
    }

})
function inputHandler(event) {
    console.log("event", event)
    event.chessboard.removeMarkers(undefined, MARKER_TYPE.dot)
    event.chessboard.removeMarkers(undefined, MARKER_TYPE.square)
    if (event.type === INPUT_EVENT_TYPE.moveStart) {
        const moves = chess.moves({square: event.square, verbose: true});
        event.chessboard.addMarker(event.square, MARKER_TYPE.square)
        for (const move of moves) {
            event.chessboard.addMarker(move.to, MARKER_TYPE.dot)
        }
        return moves.length > 0
    } else if (event.type === INPUT_EVENT_TYPE.moveDone) {
        const move = {from: event.squareFrom, to: event.squareTo}
        const result = chess.move(move)
        if (result) {
            event.chessboard.removeMarkers(undefined, MARKER_TYPE.square)
            event.chessboard.disableMoveInput()
            event.chessboard.setPosition(chess.fen())
            socket.send(JSON.stringify({
                "event": "MOVE",
                "message": {'fen':chess.fen()}
            }

            ))
            const possibleMoves = chess.moves({verbose: true})
            if (possibleMoves.length > 0) {
                const randomIndex = Math.floor(Math.random() * possibleMoves.length)
                const randomMove = possibleMoves[randomIndex]
                setTimeout(() => { // smoother with 500ms delay
                    chess.move({from: randomMove.from, to: randomMove.to})
                    event.chessboard.enableMoveInput(inputHandler, COLOR.white)
                    event.chessboard.setPosition(chess.fen())
                    socket.send(JSON.stringify({
                        "event": "MOVE",
                        "message": {'fen':chess.fen()}
                    }))
                }, 500)
            }
        } else {
            console.warn("invalid move", move)
        }
        return result
    }
}

board.enableMoveInput(inputHandler, COLOR.white)





console.log(socket)

var status = $('#status')
var fen = $('#fen')
var $pgn = $('#pgn')




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
                
                break;

            case "END":
                alert(message);
                
                break;
            case "MOVE":
                //movesCount +=1
                chess.load(message['fen'])
                board.setPosition(message['fen'])
                
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




