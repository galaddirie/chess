import imageConfig from '../config/images.js'
export class Board{
    constructor(gameConfig){
        this.table = this.initlizeBoard()
        this.table_id = //uuid
        this.populate(gameConfig)
    }
    initlizeBoard(){
    
        var board = document.createElement('div');
        board.className = 'board isPLayingWhite'
        var cells = 8
        var rows = 8
        var letters = ['a','b','c','d','e','f','g','h',]
        
    
        for (var i = 1; i <= rows; i++) {
            var row = document.createElement('div');
            row.className = 'row'
            
            for (var j = 1; j <=cells; j++) {
                var cell = document.createElement('div');
                cell.id = letters[j-1] + String(i)
                var celltextNum = document.createElement('div')
                var celltextLetter = document.createElement('div')
                if(j== 1){
                    celltextNum.append(String(i))
                    celltextNum.className = 'notation-num'
                    cell.appendChild(celltextNum)
                }
                if(i == 1){
                    celltextLetter.append(letters[j-1])
                    celltextLetter.className = 'notation-letter'
                    cell.appendChild(celltextLetter)
                }
                if (i%2 == j%2) {
                    cell.className = 'cell black';  
                } else {
                    cell.className = 'cell white';
                }
                row.appendChild(cell);
            }
            board.appendChild(row);
        }
        return board
    }
    addSquareListener(){
        this.table.querySelectorAll('.cell')
    }
    populate(gameConfig){
        
        //after we initilize the board and its event listeners we will populate it with a gamestate/ pieces
        for (var id in gameConfig) {
            console.log(id)
            if (Object.hasOwnProperty.call(gameConfig, id)) {
                
                const pieceName = gameConfig[id];
                const pieceImg = document.createElement('img')
                pieceImg.src = imageConfig[pieceName]
                pieceImg.setAttribute('data-piece', pieceName)
                
                const square = this.table.querySelector('#'+id)
                console.log(square)
                square.appendChild(pieceImg)
            }
        }
    }
    move(){
        
    }
}