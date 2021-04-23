# python_game_mine_sweeper
Mine-Sweeper, a Python coded game. 

## Idea

A small adventure game. How large the board is and “easy” or “hard” mode are predefined by command line arguments. Bombs and treasures are randomly placed on the board, while other positions are empty. Player can choose position on the board he wants to go. At the beginning he has m (which is computed according to the number of bombs) lives, he’ll lose one life every time he steps on a bomb. The ultimate goal of the game is to find all treasures before dead. The game ends when player is dead or he has found all treasures. 

## Topics included

### Error handling
When game starts, the program successively prompts the user to make selections. To make sure invalid user input doesn’t cause the program to crash, I use try/except. For example, the input is expected to be numbers which will be cast into int afterwards, however the user types a letter, then except ValueError can be used to handle this issue.
### Classes/objects
I mainly defined three classes in this program, namely Board, Player, Game. 
### Numpy
Generate the board by randomly select elements with replacement from a given set, according to a given probability; generate a 1D array of zeros.
### Command line arguments
The board size n and mode (1: easy; 2: hard) are predefined by command line arguments. For example, we run the program by “$ adventure.py 4 1”
As we have constraints that n must be an integer from 4 to 9, mode must be 1 or 2, if not satisfied, it will print out 
```
Usage: python adventure.py <Board size> <Level (easy/hard)>
<Board size>: Board size should be an integer from 4-9.
<Level (easy/hard)>: Enter number for difficulty Level 1:easy, 2:hard.
```
