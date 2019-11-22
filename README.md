# Vendredi-Noir
Gesture Interface + Multiplay Tetris

## Gesture UI

## TetrisClient

## TetrisServer
`W:10 x H:20`

![block](https://livedoor.blogimg.jp/mkomiz/imgs/f/f/ff82b30d.gif)

### Requirements
- Python 3.7.5
- Flask
- Flask-SocketIO

### API schema
```json
{
  "player1": {
    "score": "120",
    "falling": {
      "type": "O",
      "pos": [3, 5]
    },
    "next": "J",
    "board": [
      [0, 0, 0, ...],
      [0, 0, 0, ...],
      ...
      [0, 1, 2, ...],
    ],
    "isDead": false
  },
  "player2": {
    ...
  }
}
```

### 参考
<https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/app.py>