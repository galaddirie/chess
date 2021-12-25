import imageConfig from './config/images.js'
import {INPUT_EVENT_TYPE, Chessboard, COLOR, BORDER_TYPE, MARKER_TYPE} from './../../vendor/cm-chessboard/src/cm-chessboard/Chessboard.js'



var matchId = JSON.parse(document.getElementById('game-id').textContent);
var socket = new WebSocket('ws://'+ window.location.host + '/game/' + matchId + '/')

var chess = new Chess()
var board = new Chessboard(document.getElementById("chessboard"),{
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
    animationDuration: 10, // pieces animation duration in milliseconds
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
        const move = {from: event.squareFrom, to: event.squareTo, promotion:'q'}
        const moves = chess.moves({square: event.squareFrom, verbose:true})
        var valid = false
        for(let validMove in moves){
            if (moves[validMove].to == event.squareTo){
                valid = true
                // 
            }
        }
        if (valid){
            event.chessboard.removeMarkers(undefined, MARKER_TYPE.square)
            //event.chessboard.disableMoveInput()
            //event.chessboard.setPosition(chess.fen())
            socket.send(JSON.stringify({
                "event": "MOVE",
                "message": {'fen':chess.fen(),'move':move, 'pgn':chess.pgn()}
            }))     
        } else {
            console.warn("invalid move", move)
        }
        return valid
    }
}

var status = $('#status')
var fenContainer = document.getElementById('fen')
var pgnContainer = document.getElementById('pgn')

function updateStatus(){
    console.log(chess.pgn())
    pgnContainer.innerHTML= chess.pgn({ max_width: 5, newline_char: '<br />' })
    fenContainer.innerHTML = chess.fen()
}
//TODO WE NEED TO HANDLE setOrientation , enableMoveInput(inputHandler, COLOR), AND USER AUTHENTICATION WHEN MAKING MOVES,
// WE ALSO NEED A TIMER MODULE THAT WORKS IN TANDEM I.E WE WILL START TIMER FOR THE OTHER PLAYER ON RECIVING OF MOVE EVENT ,  
// IF THE PLAYER DOESNT HAVE AN ACCOUNT WE MIGHT NEED TO USE SESSION ID TO VALIDATE WHO IS MAKING THE MOVES, AND FOR ANYONE ELSE
// WHO LOADS INTO THE PAGE WE disableMoveInput()
// WE ALSO MUST ONLY START THE GAME WHEN TWO PLAYERS ARE CONNECTED
//board.enableMoveInput(inputHandler)//, COLOR['white'])





let GameState, Player, GameBoard
 



function connect() {
    socket.onopen = function open() {
        console.log('WebSockets connection created.');
        socket.send(JSON.stringify({
            "event": "CONNECT",
        }));
    };

    // Sending the info about the room
    socket.onmessage = function (e) {
        // On getting the message from the server
        // Do the appropriate steps on each event.
        let data = JSON.parse(e.data);
        
        data = data["payload"];
        let message = data['content'];
        let event = data["event"];
        console.log(data)
        switch (event) {
            case "CONNECT":

                chess.load(message['fen'])
                const boardState = chess.fen()
                board.setPosition(boardState)
                updateStatus()
                ```
                initilize chess engine and board
                initilize GameState and player
                defult orientation will be white
                if game is open
                    if player == game.creator
                        render Waiting for player overlay
                    render join btn
                if game is not open
                    if player == game.white
                        board.enableMoveInput(inputHandler, COLOR['white'])
                    if player == game.black
                        board.setOrientation = 'black
                        board.enableMoveInput(inputHandler, COLOR['black'])  
                    else:
                        board.disableMoveInput
                        
                ```
                
               
                board.enableMoveInput(inputHandler) 
                break;
            case "JOIN":
                ```
                
                onJoin
                    disable Join btn
                    reset chess engine, reset boards to initial position
                    // we will re run this following  code to make sure we initilize the board properly on the new game edge case
                    if player == game.white
                        board.enableMoveInput(inputHandler, COLOR['white'])
                    if player == game.black
                        board.setOrientation = 'black
                        board.enableMoveInput(inputHandler, COLOR['black'])  
                    else:
                        board.disableMoveInput
                    //

                ```
            case "END":
                ```
                alert(message);
                display winner
                close socket connections
                ```
                break;

            case "MOVE":
                //movesCount +=1
                console.log('reviced move')
                chess.move(message['move'])
                board.setPosition(chess.fen())
                updateStatus()
                ```
                set move
                if chess.game_over
                    if chess.in_checkmate
                        send alert winner
                    if chess.in_draw or chess.insufficient_material
                        send alert draw
                    if chess.in_stalemate
                        send alert stalemate
                    if chess.in_threefold_repetition()
                        send alert threefold rep 
                    
                    
                    
                ```
                break;
            default:
                console.log(data)
        }
    };

    socket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };
    if (socket.readyState == WebSocket.OPEN) {
        socket.onopen();
    }
}

connect();






