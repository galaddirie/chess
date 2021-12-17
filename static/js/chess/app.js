import {Game} from './logic/Game.js'
import gameConfig from './config/initalGame.js'

function createBoard(){
    
    var board = document.createElement('div');
    board.className = 'board'
    var cells = 8
    var rows = 8
    var letters = ['a','b','c','d','e','f','g','h',]
    
    // var header = document.createElement('div');
    // header.className = 'row'
    // header.innerHTML="<div class='cell'></div>"
    // for (let i = 0; i < letters.length; i++) {
    //     const j = letters[i];
    //     var cell = document.createElement('div');
    //     cell.className = 'cell columnID'
    //     cell.append(String(j).toUpperCase())
    //     header.appendChild(cell)
        
    // }
    // board.appendChild(header)

    for (var i = 1; i <= rows; i++) {
        var row = document.createElement('div');
        row.className = 'row'
        // row.innerHTML="<div class='cell rowID'>"+i+'</div>'
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
                cell.className = 'cell inPlay black';  
            } else {
                cell.className = 'cell inPlay white';
            }
            row.appendChild(cell);
        }
        board.appendChild(row);
    }
    
    console.log(board)
    return board
}
var game = document.getElementById('game')
game.appendChild(createBoard());

game = new Game(true, gameConfig)