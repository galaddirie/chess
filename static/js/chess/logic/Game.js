
import {Square} from './Square.js'
import {Piece} from './Piece.js'
import imageConfig from '../config/images.js'
export class Game{
    constructor(isWhite, gameConfig){
        this.isWhite = isWhite
        this.board = this.generateBoard(gameConfig)
        this.whiteInCheck = false
        this.blackInCheck = false
    }
    generateBoard(gameConfig){
        //generate the board the inital piece setup in the gameConfig
        // generate in the perspective of the player i.e if white reverse .
        // since we are appending from top to bottom where bottom is the perspective of the player and white starts at 1
        var letters = ['a','b','c','d','e','f','g','h',]
        var table = []
        for (let i = 1; i <=8 ; i++) {
            table.push([])
            for (let j = 1; j <=8; j++) {
                const id = letters[j-1] + String(i)
                var piece = null
                if (id in gameConfig){
                    const initalPiece = gameConfig[id].split('_')
                    const name =initalPiece[1], 
                    color = initalPiece[0]
                    const image = imageConfig[gameConfig[id]]
                    piece = new Piece(name, id, false, color,image) 
                }
                const cell = new Square(id, piece)
                table[i-1].push(cell)
            }
        }
        console.log(table)
        if (this.isWhite){
            table = table.reverse()
        }
        return table
    }
    movePiece(currSquare, endSquare){
        // validate move here rather than the ui because a player could by pass the ui with console
    }
}
