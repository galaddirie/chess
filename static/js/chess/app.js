import imageConfig from './config/images.js'
import {INPUT_EVENT_TYPE, Chessboard, COLOR, BORDER_TYPE, MARKER_TYPE} from './../../vendor/cm-chessboard/src/cm-chessboard/Chessboard.js'

var matchId = JSON.parse(document.getElementById('game-id').textContent),
    playerId = JSON.parse(document.getElementById('player-id').textContent)

let GameState, 
    Player,
    socket = new WebSocket('ws://'+ window.location.host + '/game/' + matchId + '/')

let connected = false,
    players = [] 

var status = document.getElementById('status'),
    fenContainer = document.getElementById('fen'),
    pgnContainer = document.getElementById('pgn')


var chess = new Chess(),
    board = new Chessboard(document.getElementById("chessboard"),{
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
        animationDuration: 200, // pieces animation duration in milliseconds
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
            // THE ISSUE IS WE ARE SENDING THE GAME STATE BEFORE THE MOVE IS MADE
            chess.move(move)
                //board.setPosition(chess.fen())
            GameState.pgn = chess.pgn()
            GameState.fen = chess.fen()
            event.chessboard.removeMarkers(undefined, MARKER_TYPE.square)
            socket.send(JSON.stringify({
                "event": "MOVE",
                "message": {'game': GameState,'move':move}
            }))     
        } else {
            console.warn("invalid move", move)
        }
        return valid
    }
}


//TODO WE NEED TO HANDLE setOrientation , enableMoveInput(inputHandler, COLOR), AND USER AUTHENTICATION WHEN MAKING MOVES,
// WE ALSO NEED A TIMER MODULE THAT WORKS IN TANDEM I.E WE WILL START TIMER FOR THE OTHER PLAYER ON RECIVING OF MOVE EVENT ,  
// IF THE PLAYER DOESNT HAVE AN ACCOUNT WE MIGHT NEED TO USE SESSION ID TO VALIDATE WHO IS MAKING THE MOVES, AND FOR ANYONE ELSE
// WHO LOADS INTO THE PAGE WE disableMoveInput()
// WE ALSO MUST ONLY START THE GAME WHEN TWO PLAYERS ARE CONNECTED
//board.enableMoveInput(inputHandler)//, COLOR['white'])







let joinBtn = document.getElementById('joinBtn'),
    playerWaiting = document.getElementById('playerWait')
joinBtn.addEventListener('click', joinGame)

function joinGame(){
    if (GameState.openGame){
        GameState.openGame = false
        GameState.opponent = playerId

        if (GameState.white==null){
            
            GameState.white = playerId
        }else{
            GameState.black = playerId
        }
        socket.send(JSON.stringify({
            "event": "JOIN",
            "message": {"game":GameState}
        }));
    }
    
}

// HELPER FUNCTIONS
function ComparePlayer(player1, player2){
    return (player1.player_id == player2.player_id)
}

function updateStatus(){
    pgnContainer.innerHTML= chess.pgn({ max_width: 5, newline_char: '<br />' })
    fenContainer.innerHTML = chess.fen()
}

function initilizeBoard(game,player){
    console.log(player)
    chess.load_pgn(game.pgn)
    board.setPosition(chess.fen())
    updateStatus()
    
    if (ComparePlayer(player, game.white)){
        board.enableMoveInput(inputHandler, COLOR['white'])
    }
    else if (ComparePlayer(player, game.black)){
        board.enableMoveInput(inputHandler, COLOR['black'])
        board.setOrientation(COLOR.black)
    }
    
    else{
        board.disableMoveInput
    }

}
    

function connect() {
    socket.onopen = function open() {
        console.log('WebSockets connection created.');
        console.log(playerId)
        socket.send(JSON.stringify({
            "event": "CONNECT",
            "message": {"player":playerId}
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

        GameState = message['game']
        
        switch (event) {
            case "CONNECT":
                if (!Player){
                    //NOTE 
                    // caeful assigning user dependant variables like this 
                    // all connected parties will have their variable over written 
                    // since it is being broadcasted this isnt an issue 
                    // when we send user specific data to their personal channels
                    // but since we are notifying all parties that someone connected it is
                    // we could consider chaining events but might get messy

                    Player = message['player']
                }
                //players.push (Player) // we need to get active members in the grooup from server instead since this vbreaks on relod
            
                // this will only change anything if we change connected event channel group name
                
                
                console.log(GameState)
                if (GameState.openGame){//TODO REMOVE !
                    console.log('JOIN GAME')
                    if (ComparePlayer(Player, GameState.creator)){// we will add a unique id to the profile when we send the data
                        playerWaiting.hidden = false
                    }else{

                        console.log('JOIN GAME')
                        joinBtn.hidden = false
                    } 
                }
                initilizeBoard(GameState, Player)
                
                connected = true
                //remove this later
                //board.enableMoveInput(inputHandler) 
                break;

            case "JOIN":
                joinBtn.hidden = true
                playerWaiting.hidden = true
                initilizeBoard(GameState, Player)
                break

                
            case "END":
                // ```
                // alert(message);
                // display winner
                // close socket connections
                // ```
                break;

            case "MOVE":
                //movesCount +=1
                console.log('reviced move')
                chess.move(message['move'])
                board.setPosition(chess.fen())
                updateStatus()
                // ```
                // set move
                // if chess.game_over
                //     if chess.in_checkmate
                //         send alert winner
                //     if chess.in_draw or chess.insufficient_material
                //         send alert draw
                //     if chess.in_stalemate
                //         send alert stalemate
                //     if chess.in_threefold_repetition()
                //         send alert threefold rep 
                    
                    
                // ```
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






