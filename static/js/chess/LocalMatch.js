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
        responsive: true,
         // resizes the board based on element size
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
            chess.move(move)
            board.setPosition(chess.fen())
            updateStatus()
            event.chessboard.removeMarkers(undefined, MARKER_TYPE.square)
            
            
            
        } else {
            console.warn("invalid move", move)
        }
        return valid
    }
}

function updateStatus(){
    pgnContainer.innerHTML= chess.pgn({ max_width: 20, newline_char: '<br />' })
    //fenContainer.innerHTML = chess.fen()

    var color = ''
    if(chess.turn() == 'b'){
        color = 'Black '
    }else{
        color = 'White '
    }

    var status = ''
    if(chess.in_check()){
        status = 'in check.'
    }
    else if (chess.in_checkmate()){
        status = 'has Lost'
    }
    else{
        status = 'to move.'
    }
    statusContainer.innerHTML = color + status
}
