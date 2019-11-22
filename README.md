# Vendredi-Noir
Gesture Interface + Multiplay Tetris

## Tetris
`W:10 x H:10`

![block](https://livedoor.blogimg.jp/mkomiz/imgs/f/f/ff82b30d.gif)


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