"https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js" 
var AudioSpites = new Howl({
    src: ['https://chess-stream.storage.googleapis.com/static/audio/sprites.mp3'],
    sprite: {
        "game_start":   [ 0*1000,  0.9*1000],
        "game_won":     [ 0.9*1000,  1.8*1000],
        "game_lost":    [ 2.7*1000,  0.9*1000],
        "game_draw":    [ 9.45*1000,  1.35*1000],
        "check":        [ 3.6*1000,  0.45*1000],
        "wrong_move":   [ 4.05*1000,  0.45*1000],
        "move":         [ 4.5*1000,  0.2*1000],
        "capture":      [ 6.3*1000,  0.2*1000],
        "castle":       [ 7.65*1000,  0.2*1000],
        "take_back":    [ 8.1*1000,  0.12*1000],
        "promotion":    [ 9.0*1000,  0.45*1000],
        "dialog":       [ 10.8*1000,  0.45*1000]
      }
});

export{AudioSpites}