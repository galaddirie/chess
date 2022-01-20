/**
 * object-orientated refactor of OnelineMatch.js  
 */
import { INPUT_EVENT_TYPE, Chessboard, COLOR, BORDER_TYPE, MARKER_TYPE } from '../../vendor/cm-chessboard/src/cm-chessboard/Chessboard.js'
import { AudioSpites } from './AudioSprites.js'

AudioSpites.once('load', function () {
    AudioSpites.play();
});

let MID = JSON.parse(document.getElementById('game-id').textContent),
    PID = JSON.parse(document.getElementById('player-id').textContent)

let USER = new Player(PID)

let COLORS = { 'b': "Black", 'w': 'White' }

class Color {
    constructor() {
        this.displayName
        this.type
        this.id
    }
}

class Player {
    constructor(playerId) {
        this.playerId = playerId
        this.playerData = {}
        this.color = new Color
    }
}

class Game {
    constructor() {
        this.participants = {}
        this.matchId = MID
        this.chess = new Chess()
        this.board = new Chessboard(document.getElementById("chessboard"), {
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
        this.gameState
        this.user = USER // refrence to the user in client
        this.status = {
            color: '',
            state: ''
        }
    }

    inputHandler(event) {
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
                this.makeMove(move, false)

                socket.send(JSON.stringify({
                    "event": "MOVE",
                    "message": {
                        'gameUpdates': {
                            'fen': this.gameState.fen,
                            'pgn': this.gameState.pgn,
                            'completed': this.gameState.completed,
                            'winner': this.gameState.winner,
                        },
                        'move': move, 'movePlayer': this.user.playerData
                    }
                }))
            } else {
                console.warn("invalid move", move)
                AudioSpites.play('take_back')
            }
            return valid
        }
    }

    setGame(game) {
        this.gameState = game
        this.chess.load_pgn(game.pgn)
        this.board.setPosition(this.chess.fen())
    }

    makeMove(move, server) {
        if (!server || this.user.color.id == this.chess.turn()) {
            this.chess.move(move)
            this.board.setPosition(this.chess.fen())
            this.gameState.pgn = this.chess.pgn
            this.gameState.fen = this.chess.fen
        }
        this.render()
    }

    isParticipant(playerId) {
        return playerId in this.participants
    }

    getPlayerFromColor(color_id) {
        for (playerId in this.participants) {
            if (color_id == this.participants[playerId].color.id) {
                return this.participants[playerId]
            }
        }
    }

    getOpponent(player) {
        for (playerId in this.participants) {
            if (player.playerId != playerId) {
                return this.participants[playerId]
            }
        }

    }

    intilizeBoard() {
        this.chess.load_pgn(game.pgn)
        if (!this.gameState.openGame) {
            if (this.isParticipant(this.user.playerId)) {
                board.enableMoveInput(this.inputHandler, this.user.color.type)
            }

        } else {
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

    render() {
        if (this.chess.game_over()) {
            this.gameState.completed = true

            let last_player = this.participants[
                this.chess.turn() == 'b' ?
                    this.gameState.white : this.gameState.black
            ]

            if (this.chess.in_checkmate()) {
                this.gameState.winner = last_player.playerData
                if (this.user.color.id == this.chess.turn()) {
                    AudioSpites.play('game_lost')
                } else {
                    AudioSpites.play('game_won')
                }
                this.status.color = COLORS[this.chess.turn()]
                this.status.state = 'in checkmate.'

            }
            else if (this.chess.in_draw() || this.chess.in_stalemate()) {
                AudioSpites.play('game_draw')
                this.status.color = last_player.color.displayName
                this.status.state = 'has drawn'

            }
            winModal.show()

        }
        else if (this.chess.in_check()) {
            AudioSpites.play('check')
            this.status.state = 'in Check'
        }
        else {
            AudioSpites.play('move')
            this.status.state = 'to move.'
        }
    }

}

class GameWebSocket {
    constructor() {
        this.socket = new WebSocket('ws://' + window.location.host + '/game/' + MID + '/')
        this.game = new Game()
        this.user = USER
        this.participants
        this.activeUsers
        this.connected = false
        this.initlizeSocket()


    }
    initlizeSocket() {
        this.socket.onopen = this.onOpen
        this.socket.onmessage = this.onMessage
        this.socket.onclose = this.onClose
        if (this.socket.readyState == WebSocket.OPEN) {
            this.socket.onopen();
        }
    }

    onOpen() {
        console.log('WebSockets connection created.');
        this.socket.send(JSON.stringify({
            "event": "CONNECT",
            "message": { "player": PID }
        }));
    }

    onMessage(e) {
        let data = JSON.parse(e.data);
        let message = data['message'];
        let event = data["event"];
        console.log(data)
        if (message['gameUpdates']) {
            for (const [key, value] of Object.entries(message['gameUpdates']))
                this.game.gameState[key] = value
        }
        if (message['game']) {
            this.game.gameState = message['game']
        }

        switch (event) {
            case "MOVE":
                this.game.makeMove(message['move'], true)
                if (this.gameState.completed != null) {
                    socket.onclose()
                }
                break;

            case "CONNECT":
                if (!this.user.playerData && message['player']['player_id'] == this.user.playerId) {
                    this.user.playerData = message['player']
                }
                if (!this.connected) {
                    this.game.initilizeBoard()
                }
                this.connected = true
                break;

            case "JOIN":
                this.game.initilizeBoard()
                break

            case "END":

                break;
            default:
            //
        }
    }

    onClose(e) {
        console.log('Socket is closed. Reconnect will be attempted in 5 second.', e.reason);
        this.connected = false
        setTimeout(function () {
            this.initlize();
        }, 5000);
    }

    joinGame() {
        if (this.game.gameState.openGame) {
            this.game.gameState.openGame = false
            this.game.gameState.opponent = PID

            if (this.game.gameState.white == null) {
                this.game.gameState.white = PID
            } else {
                this.game.gameState.black = PID
            }
            this.socket.send(JSON.stringify({
                "event": "JOIN",
                "message": { "game": this.game.gameState }
            }));
        }

    }

}   