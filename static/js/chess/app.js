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
var $status = $('#status')
var $fen = $('#fen')
var $pgn = $('#pgn')
var myturn = true;

function onDragStart (source, piece, position, orientation) {
    // do not pick up pieces if the game is over
    if (game.game_over()) return false
    
    // only pick up pieces for the side to move
    if (!myturn || (game.turn() === 'w' && piece.search(/^b/) !== -1) || (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
        return false
    }
    var moves = game.moves({square: source, verbose: true})
    for(let i in moves){
            let move = moves[i]
            const el = document.querySelector(`div[data-square="${move['to']}"]`)
            el.classList.add('valid-moves')
            console.log(el)

    }
    
    
}

function onDrop (source, target) {
    // see if the move is legal
    var move = game.move({
        from: source,
        to: target,
        promotion: 'q' // NOTE: always promote to a queen for example simplicity
    })
    
    console.log(move)
    // illegal move
    if (move === null) return 'snapback'
    let data = {
        "event": "MOVE",
        "message": {
            "fen":game.fen(),
            "player": 'player'
        }
    }
    socket.send(JSON.stringify(data))
    updateStatus()
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
    
    board.position(game.fen())
}

let win = false
function updateStatus () {
    var status = ''
    var moveColor = 'White'
    
    if (game.turn() === 'b') {
        moveColor = 'Black'
    }
    
    // checkmate?
    if (game.in_checkmate()) {
        status = 'Game over, ' + moveColor + ' is in checkmate.'
        
    }
    
    // draw?
    else if (game.in_draw()) {
        status = 'Game over, drawn position'
    }
    
    // game still on
    else {
        status = moveColor + ' to move'
    
        // check?
        if (game.in_check()) {
        status += ', ' + moveColor + ' is in check'
        }
    }
    
    $status.html(status)
    $fen.html(game.fen())
    //$pgn.html(game.pgn())
}

function initlize(){
    
    game = new Chess()
    var $status = $('#status')
    var $fen = $('#fen')
    var $pgn = $('#pgn')

    

    function pieceTheme (piece) {
        if (piece in imageConfig){
            return imageConfig[piece]
        }
    }
    var config = {
        pieceTheme: pieceTheme,
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd,
        draggable: true,
        position: 'start',
    }
    board = new Chessboard('myBoard', config)
    // TODO ADD ON CLICK EVENT LISTENER TO ALL
    //ON CLICK WE WILL STORE A TO VALUE, IF WE DROP 
    //$(window).resize(board.resize)
    updateStatus()

      
}

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
        
        data = data["payload"];
        let message = data['content'];
        let event = data["event"];
        console.log(message)
        switch (event) {
            case "START":
                initlize();
                break;
            case "END":
                alert(message);
                initlize();
                break;
            case "MOVE":
                game.load(message['fen'])
                board.position(message['fen'])
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




