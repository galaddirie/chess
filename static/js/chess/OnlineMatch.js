import { INPUT_EVENT_TYPE, Chessboard, COLOR, BORDER_TYPE, MARKER_TYPE } from '../../vendor/cm-chessboard/src/cm-chessboard/Chessboard.js'
import { AudioSpites } from './AudioSprites.js'

AudioSpites.once('load', function () {
    AudioSpites.play();
});


var matchId = JSON.parse(document.getElementById('game-id').textContent),
    playerId = JSON.parse(document.getElementById('player-id').textContent)

let GameState,
    Player,
    socket = new WebSocket('ws://' + window.location.host + '/game/' + matchId + '/')

let connected = false,
    players = []

var gameContainer = document.getElementById('gameContainer'),
    statusContainer = document.getElementById('status'),
    //fenContainer = document.getElementById('fen'),
    pgnContainer = document.getElementById('pgn')

var playerSelfName = document.getElementById('playerSelfName'),
    playerSelfImage = document.getElementById('playerSelfImage')

var playerOppName = document.getElementById('playerOppName'),
    playerOppImage = document.getElementById('playerOppImage')

var chess = new Chess(),
    board = new Chessboard(document.getElementById("chessboard"), {
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
        responsive: true,
        // resizes the board based on element size
        animationDuration: 200, // pieces animation duration in milliseconds
        sprite: {
            url: "./../../static/vendor/cm-chessboard/assets/images/chessboard-sprite-staunty.svg", // pieces and markers are stored as svg sprite
            size: 40, // the sprite size, defaults to 40x40px
            cache: true // cache the sprite inline, in the HTML
        }

    })

// code snippet from cm-chessboard example
// https://shaack.com/projekte/cm-chessboard/examples/validate-moves.html
function inputHandler(event) {
    event.chessboard.removeMarkers(undefined, MARKER_TYPE.dot)
    event.chessboard.removeMarkers(undefined, MARKER_TYPE.square)
    if (event.type === INPUT_EVENT_TYPE.moveStart) {
        const moves = chess.moves({ square: event.square, verbose: true });
        event.chessboard.addMarker(event.square, MARKER_TYPE.square)
        for (const move of moves) {
            event.chessboard.addMarker(move.to, MARKER_TYPE.dot)
        }
        return moves.length > 0
    } else if (event.type === INPUT_EVENT_TYPE.moveDone) {
        const move = { from: event.squareFrom, to: event.squareTo, promotion: 'q' }
        const moves = chess.moves({ square: event.squareFrom, verbose: true })
        var valid = false
        for (let validMove in moves) {
            if (moves[validMove].to == event.squareTo) {
                valid = true
            }
        }
        if (valid) {
            event.chessboard.removeMarkers(undefined, MARKER_TYPE.square)
            moveHandler(move, Player, false)



            socket.send(JSON.stringify({
                "event": "MOVE",
                "message": { 'game': GameState, 'move': move, 'movePlayer': Player }
            }))
        } else {
            console.warn("invalid move", move)
            AudioSpites.play('take_back')
        }
        return valid
    }
}



let joinBtn = document.getElementById('joinBtn'),
    playerWaiting = document.getElementById('playerWait'),
    openGame = document.getElementById('openGame')
joinBtn.addEventListener('click', joinGame)

function joinGame() {
    if (GameState.openGame) {
        GameState.openGame = false
        GameState.opponent = playerId

        if (GameState.white == null) {
            GameState.white = playerId
        } else {
            GameState.black = playerId
        }
        socket.send(JSON.stringify({
            "event": "JOIN",
            "message": { "game": GameState }
        }));
    }

}

// HELPER FUNCTIONS
function ComparePlayer(player1, player2) {
    return (player1.player_id == player2.player_id)
}

function determineWin(color) {
    if (playerId == GameState[color].player_id) {
        AudioSpites.play('game_lost')
        return 'lost'
    }
    else {
        AudioSpites.play('game_won')
    }
}

function moveHandler(move, movePlayer, server) {

    if (!server || (movePlayer.player_id != playerId)) {
        chess.move(move)
        board.setPosition(chess.fen())
        GameState.pgn = chess.pgn()
        GameState.fen = chess.fen()


        if (chess.game_over()) {
            GameState.completed = true
            if (chess.in_checkmate()) {

                if (chess.turn() == 'b') {
                    determineWin('black')
                    GameState.winner = GameState.white
                    modalText.innerHTML = 'White s Won';

                }
                else {
                    determineWin('white')
                    GameState.winner = GameState.black
                    modalText.innerHTML = 'Black has Won';
                }

            }
            else if (chess.in_draw() || chess.in_stalemate()) {
                AudioSpites.play('game_draw')
                modalText.innerHTML = 'Draw!';

            }
            winModal.show()

        }

        else if (chess.in_check()) {
            AudioSpites.play('check')
        }
        else {
            AudioSpites.play('move')

        }
    }
}


var winModal = new bootstrap.Modal(document.getElementById('winPopup')),
    modalText = document.getElementById('winPopupText')

function updateStatus() {
    pgnContainer.innerHTML = chess.pgn({ max_width: 5, newline_char: '<br />' })
    //fenContainer.innerHTML = chess.fen()

    var color = ''
    if (chess.turn() == 'b') {
        color = 'Black '
    } else {
        color = 'White '
    }

    var status = ''
    //NOTE REPEATE CODE FROM mOVE hANDLER
    if (chess.game_over()) {
        if (chess.in_checkmate()) {
            status = 'has lost'
        }
        else if (chess.in_draw() || chess.in_stalemate()) {
            status = 'has drawn.'
        }
        else {
            status = 'has won.'
        }
    }
    else if (chess.in_check()) {

        status = 'in check.'
    }
    else {
        status = 'to move.'
    }
    statusContainer.innerHTML = color + status
}

function renderPlayerDetails(player, name, image) {
    if (player.user != null) {
        name.innerHTML = player.user.username
    } else {
        name.innerHTML = 'Anonymous Player'
    }
    image.src = player.image
}

function initilizeBoard(game, player) {
    chess.load_pgn(game.pgn)

    updateStatus()
    if (!game.openGame) {
        gameContainer.hidden = false
        openGame.hidden = true
        if (ComparePlayer(player, game.white)) {
            board.enableMoveInput(inputHandler, COLOR['white'])
            renderPlayerDetails(player, playerSelfName, playerSelfImage)
            renderPlayerDetails(game.black, playerOppName, playerOppImage)
        }
        else if (ComparePlayer(player, game.black)) {
            board.enableMoveInput(inputHandler, COLOR['black'])

            renderPlayerDetails(player, playerSelfName, playerSelfImage)
            renderPlayerDetails(game.white, playerOppName, playerOppImage)

            board.setOrientation(COLOR.black)


        }
    }
    else {
        gameContainer.hidden = false
        openGame.hidden = false
        gameContainer.classList.add('inactive')
        if (ComparePlayer(Player, GameState.creator)) {// we will add a unique id to the profile when we send the data
            playerWaiting.hidden = false
        } else {
            joinBtn.hidden = false
        }
        board.disableMoveInput
    }
    setTimeout(function () {
        board.setPosition(chess.fen())
    }, 500)


}


function connect() {
    socket.onopen = function open() {
        console.log('WebSockets connection created.');
        socket.send(JSON.stringify({
            "event": "CONNECT",
            "message": { "player": playerId }
        }));
    };

    socket.onmessage = function (e) {
        let data = JSON.parse(e.data);

        let message = data['message'];
        let event = data["event"];

        GameState = message['game']

        switch (event) {
            case "MOVE":

                moveHandler(message['move'], message['movePlayer'], true)
                updateStatus()
                if (GameState.completed != null) {
                    socket.onclose()
                }

                break;

            case "CONNECT":
                if (!Player) {
                    // NOT WORKING RIGHT
                    Player = message['player']
                }
                initilizeBoard(GameState, Player)
                connected = true
                break;

            case "JOIN":
                initilizeBoard(GameState, Player)
                break

            case "END":


                // display winner
                // close socket connections
                // ```
                break;
            default:
            //
        }
    };

    socket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 5 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 5000);
    };
    if (socket.readyState == WebSocket.OPEN) {
        socket.onopen();
    }
}

connect();






export { inputHandler }