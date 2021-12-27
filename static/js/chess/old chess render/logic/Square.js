export class Square{
    constructor(id, piece){
        this.id = id
        this.piece = piece //if piece is occupying this square
    }
    remove(){
        p = this.piece
        this.piece = null
        return p
    }
}
