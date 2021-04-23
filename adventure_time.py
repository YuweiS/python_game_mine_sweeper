import math
import numpy as np
import sys
import random
# These are codes for colors. Just make the things print out looks more beautiful.
W  = '\033[0m' # normal white
R  = '\033[31m' # red
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan

def printboard(board_list):
    ''' Take in the board array and print out the n*n board, just reveal the things on positions already chosen. '''
    # print the header numbers indicating columns
    header=' '*4
    n=int(math.sqrt(len(board_list)))
    for i in range(n):
        header+=str(i+1)+' '*3
    print header
    # print other lines
    for i in range(n):
        print ' '*3+ '--- '*n
        line=str(i+1)
        for j in range(n):
            # format the line to make it looks good
            line+=' ' + '|'+'{0:>2}'.format(board_list[n*i+j])
        line+=' '+'|'
        print line
    print ' '*3+ '--- '*n


class Board(object):
    """ This class represents the borad of the game, which has positions and things on it for player to interact with. """
    def __init__(self,n,mode):
        # initialize the board with given size (n*n) and player mode (easy,hard)
        self.size=n
        self.board_list = self.create_board(n,mode) 
        self.visited=[] # list of visited places, append the index of player's choice every time player makes a move 
    def create_board(self,n,mode):
        ''' Takes in the size of board n and play mode, randomly generates 
        n^2 elements from a given set, and returns the board elements as a 1D array'''
        sets=['o','*','$']
        if mode==1: # easy
            prob=[0.6,0.2,0.2]
            # use numpy here because can set probability, more advanced than random module
            board_list=np.random.choice(sets,n**2,p=prob)         
        else: #hard
            prob=[0.2,0.4,0.4]
            board_list=np.random.choice(sets,n**2,p=prob)
        # make sure there're at least one treasure and one bomb.
        board_list[random.randint(0,n**2-1)] = "$"
        board_list[random.randint(0,n**2-1)] = "*"
        return board_list    
    def what_to_reveal(self):
        ''' A board show to the player, just reveal the things on positions already chosen. '''
        board_to_reveal=np.zeros(self.size**2,str) # initilaize
        for i in range(len(board_to_reveal)):
            if i in self.visited:
                board_to_reveal[i]=self.board_list[i]
            else:
                board_to_reveal[i]=" "
        return board_to_reveal
    def number_of_treasures(self):
        return (self.board_list=='$').sum()
    def number_of_bombs(self):
        return (self.board_list=='*').sum()      
    def has_found_alltreasures(self):
        treasure_found=0
        for i in self.visited:
            if self.board_list[i]=='$':
                treasure_found+=1
        if treasure_found==self.number_of_treasures():
            print " "
            print (C+"Congratulations! You've found all treasures!"+W)
            return True
        else:
            return False          
        
    def cal_pos(self,row,col):
        ''' After player chooses a cell (row,col), return the corresponding serial number on the board,i.e. the index of this cell in board_list '''
        index=self.size*(row-1)+(col-1)
        return index         
    def whats_in_it(self,pos):
        ''' Returns the "thing" in the position, "pos" represents the index '''
        return self.board_list[pos]   
    def record(self,pos):
        """ After player selects a position, return False if he has already selected this position before,
        return True if the position hasn't been selected once and add the position to visited list"""
        if pos in self.visited:
            return False
        else:
            self.visited.append(pos)
            return True    

    def hint(self,n,row,col):
        """ Give player hints based on position he chose"""
        # the positions in the four corners
        if row==1 and col==1:
            pos_to_check=[self.cal_pos(2,1),self.cal_pos(1,2)]
        elif row==n and col==1:
            pos_to_check=[self.cal_pos(n-1,1),self.cal_pos(n,2)]
        elif row==n and col==n:
            pos_to_check=[self.cal_pos(n-1,n),self.cal_pos(n,n-1)]
        elif row==1 and col==n:   
            pos_to_check=[self.cal_pos(1,n-1),self.cal_pos(2,n)]
        # the positions on the edges
        elif row==1 and not col in [1,n]:
            pos_to_check=[self.cal_pos(row,col-1),self.cal_pos(row,col+1),self.cal_pos(row+1,col)]
        elif row==n and not col in [1,n]:
            pos_to_check=[self.cal_pos(row,col-1),self.cal_pos(row,col+1),self.cal_pos(row-1,col)]
        elif col==1 and not row in [1,n]:
            pos_to_check=[self.cal_pos(row,col+1),self.cal_pos(row-1,col),self.cal_pos(row+1,col)]
        elif col==n and not row in [1,n]:
            pos_to_check=[self.cal_pos(row,col-1),self.cal_pos(row-1,col),self.cal_pos(row+1,col)]
        # positions in the middle
        else:
            pos_to_check=[self.cal_pos(row,col-1),self.cal_pos(row,col+1),self.cal_pos(row-1,col),self.cal_pos(row+1,col)]
        treasures_near=0
        bombs_near=0
        for i in pos_to_check:
            if self.board_list[i]=="$":
                treasures_near+=1
            if self.board_list[i]=="*":
                bombs_near+= 1
        print "Your current position is:","(",row,",",col,")"
        print " "
        print "There're",treasures_near,"treasures around you! Good luck!"
        print "There're",bombs_near,"bombs around you! Be careful!"
        

class Player(object):
    """ Player has 4 attributes, can change position (controled by user input) and interact with things on the board. """
    def __init__(self,life=3,treasures_found=0,bombs_stamped=0): # initialization
        self.life=life
        self.treasures_found=treasures_found
        self.bombs_stamped=bombs_stamped
        self.steps = 0
    
    def cal_score(self):
        """Calculate player’s score based on number of treasures/bombs he has found/stepped on, 
        and the steps he has taken. The original score is zero."""
        return self.treasures_found*10 - self.bombs_stamped*5 - 2*self.steps
    
    def choose_position(self,pos,current_board): # pos is the serial number on board, current_board is an instance of Board class
        """ Try to select a position on current board, return false if it's already selected once,
        return true if success and update other variables if needed. """
        
        if current_board.record(pos): #can choose this position, go ahead
            # interact with things on the board
            if current_board.whats_in_it(pos)=='*':
                print " "
                print (R+"Oh,no! You stepped on a bomb!"+W)
                self.bombs_stamped+=1
                self.life-=1  
            elif current_board.whats_in_it(pos)=='$':
                print " "
                print (R+"Haha! You found a treasure !"+W)
                self.treasures_found+=1
            else:
                print " "
                print (R+"Nothing in it!"+W)
            return True
        else: # This position has already been chosen once, need to select another position
            return False
      
    def print_status(self,current_board):
        """ Print player's current status: life, how many treasures found and remained, 
        how many bombs stepped on and remained """
        print "You have",self.life, "lives remained"
        print "You found",self.treasures_found,"treasures","there're still",current_board.number_of_treasures()-self.treasures_found,"treasures"
        print "You stamped on",self.bombs_stamped,"bombs","there're still",current_board.number_of_bombs()-self.bombs_stamped,"bombs"
        print "Your current score is ",self.cal_score(), " points."
    
    def isDead(self):
        """ Return True if there's no life left. """
        if self.life==0:
            print " "
            print (P+"You're dead!"+W)
            return True
        else:
            return False


class QuitError(Exception):
    """ Raise exception for “quit” command in the input. """
    pass

class InvalidInput(Exception):
    """ Indicate the input is invalid. """
    pass


class Game(object):
    """ A game with a board and a main character, i.e. the player."""
    def __init__(self, n, mode):
        print (C+"Welcome to Adventure Time!"+W)
        self.n = n
        self.mode = mode
        self.board=Board(n, mode)
        numLife = int(math.ceil(0.6*self.board.number_of_bombs()))
        self.player=Player(life = numLife)
        
    def restart(self):
        self.board=Board(self.n, self.mode)
        numLife = int(math.ceil(0.6*self.board.number_of_bombs()))
        self.player=Player(life = numLife)
        self.playGame()
                    
    def GameOver(self):
        if self.player.isDead()==True:
            return True
        elif self.board.has_found_alltreasures()==True:
            return True
        else:
            return False

    def getPos(self):
        """Prompt the player to choose a position, return player’s choice (row, col) if it’s valid.
        Raise QuitError (quit the entire game) if player types in “quit”, 
        raise InvalidInput if the player types in other thing instead of two integers like”42” representing row/col, 
        or the position is out of range. """
        choice = raw_input(
            P + "Where would you like to go? Please type in two integers representing row/column: " + W)
        if choice == "quit":
            raise QuitError
        if len(choice) != 2:
            raise InvalidInput

        try:
            row = int(choice[0])
            col = int(choice[1])
        except:
            raise InvalidInput

        if row > self.board.size or col > self.board.size:
            raise InvalidInput

        return row, col

            
    def playGame(self):
        """ Prompt the player to choose a position until the game is over. """
        while (not self.GameOver()):
            print " "
            self.player.print_status(self.board)
            print " "
            printboard(self.board.what_to_reveal())

            condition = False
            row = 0
            col = 0
            while (not condition):
                print " "
                print "Select a valid position or enter \"quit\" to quit the game."
                try:
                    row, col = self.getPos()
                except QuitError:
                    print "Quit the Game."
                    return
                except InvalidInput:
                    print "Invalid input."
                    continue
                except:
                    print "Unknown Error."
                    continue
                pos = self.board.cal_pos(row, col)
                condition = self.player.choose_position(pos, self.board)
                if not condition:
                    print "This position has been chosen once!"

            print " "
            self.player.steps += 1
            self.board.hint(self.board.size, row, col)
                
        print " "
        print "The true map is:"
        print " "
        printboard(self.board.board_list)
        self.player.print_status(self.board)
        play_again=raw_input(B+"Would you like to play again? Yes/No  Your selection: "+W)
        while  not play_again in ["Yes","No"]:
            print " Please only answer Yes or No"
            play_again=raw_input(B+"Would you like to play again? Yes/No  Your selection: "+W)
        if play_again=="Yes":
            self.restart()
            
if __name__=="__main__":
    
    correctInput = True
    # Check if command arguments are valid
    if len(sys.argv) != 3:
        correctInput = False

    size = 0
    mode = 0

    try:
        size = int(sys.argv[1])
        mode = int(sys.argv[2])
    except:
        correctInput = False

    if size < 4 or size > 9 or mode < 1 or mode > 2:
        correctInput = False

    if not correctInput:
        print C+"Usage: python adventure.py <Board size> <Level (easy/hard)>"+W
        print C+"<Board size>: Board size should be an integer from 4-9."+W
        print C+"<Level (easy/hard)>: Enter number for difficulty Level 1:easy, 2:hard."+W
    else:
        game=Game(size, mode)
        game.playGame()

