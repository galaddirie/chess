class Piece{
    constructor(name, id, isAttacked, color){
        this.name = name
        this.color = color
        this.id = id
        this.isAttacked = isAttacked
        this.moveSet = [] // an array of Squares
    }
    set(id){
        this.id = id
    }
    get(){
        // get this pieces current location
        return this.id
    }
}