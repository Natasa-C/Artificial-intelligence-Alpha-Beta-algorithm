# Artificial-intelligence-Alpha-Beta-algorithm
### Games as search problems

## English draughts
### Defining the challenge

The rules of the game are as follows:

- The game is between two players. One of them plays with white, the other with black (we can consider for the pieces the symbols a and n).

- The game board is an 8X8 size grid. Consider the lines numbered from 0 to 7 and the columns from a to h. The pieces are positioned as in the picture:

<img src="https://user-images.githubusercontent.com/57111995/86345750-9d4c5b80-bc64-11ea-9194-46695eae8000.jpg" data-canonical-src="https://user-images.githubusercontent.com/57111995/86345750-9d4c5b80-bc64-11ea-9194-46695eae8000.jpg" width="300" height="300" /> [image source](https://www.vectorstock.com/royalty-free-vector/board-with-checkers-vector-3523363)

- The pieces move diagonally (only on the dark squares on the grid)

- A player may place a single piece (of the color he has chosen to play with) when it is his turn, in a free location on the board.

- The player with black pieces moves first.

- A player J can position a piece P either with a position further diagonally (down for white and up for black) or by capturing a piece of the other player (in order to capture a piece, it must be adjacent to the diagonal with piece P and to have a free box on the diagonal, after it, as many successive captures can be made (but all possible captures must be made from that sequence).

- If a piece reaches the row at the opposite end, it becomes "king". Kings obey the same rules, but can move diagonally backwards (both in simple steps and in capture), not just before the simple pieces. Kings will be marked with A for white pieces and with N for black pieces.

- If a player cannot place any piece, or has lost all his pieces, he loses the game, the opponent becoming the winner

### Playing the game
The game can be played from the terminal.

The player can choose:
- the algorithm used by the computer: Minimax or Alpha-Beta
- the difficulty of the game: beginner, intermediate, advanced
- the heuristic
- wether it wants the black or the white pieces

| <img src="https://user-images.githubusercontent.com/57111995/86347731-61ff5c00-bc67-11ea-9e25-bcec77485a81.png" data-canonical-src="https://user-images.githubusercontent.com/57111995/86347731-61ff5c00-bc67-11ea-9e25-bcec77485a81.png" width="500" height="600" />  | <img src="https://user-images.githubusercontent.com/57111995/86347732-6297f280-bc67-11ea-9c81-183cf1ae8692.png" data-canonical-src="https://user-images.githubusercontent.com/57111995/86347732-6297f280-bc67-11ea-9c81-183cf1ae8692.png" width="500" height="600" /> |
|-|-|

### Obs: the code and comments are made in romanian.
