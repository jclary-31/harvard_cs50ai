"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
           [EMPTY, EMPTY, EMPTY]]

#    return [[EMPTY, EMPTY,X],
 #           [EMPTY, O, X],
 #           [EMPTY, EMPTY, O]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
#    raise NotImplementedError
    count_notempty=0
    for i in range(len(board)):
        for j in range(len(board[0])): 
            if board[i][j] != EMPTY:
                count_notempty+=1

    if count_notempty%2==1:
        nextplayer=O
    else:
        nextplayer=X   

    #suppose player X plays alsways first
    if count_notempty==9:
        nextplayer=O

    return nextplayer

    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    positions=set()
    for i in range(len(board)):
        for j in range(len(board[0])): 
            if board[i][j]==EMPTY: #free space
                positions.add( (i,j) )

    return positions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
  #  print (board,action)
    if terminal(board):
        return board
    
    #if game not ended action is a non empty (i,j)
    #action=(i,j)
    i=action[0]
    j=action[1]

    if i<0 or j<0: #i,j must be positive, added beacause of check50 verif
        raise Exception('NegativePosition')

    if len(action)==0: #no more free place
        raise Exception('BoardIsFull')

    if board[i][j]!=EMPTY:#place is already filled
        raise Exception('AlreadyOccupied')
    
    board2=copy.deepcopy(board)
    board2[i][j]=player(board)

    return board2

def column(matrix,i):
    #get column i in a 2d matrix.
    col=[]
    for row in matrix:
         col.append(row[i])
    return col

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    board2=copy.deepcopy(board)
    #need to change nonetype by a str here
    for i in range(len(board2)):
        for j in range(len(board2)):
            if board2[i][j]==EMPTY:
                board2[i][j]='n'

    ####all possible case are stored in situation    
    situation=[]

    #get info on lines
#    for i in range(len(board)):
#        situation.append(''.join(board2[:][i]))

    #get info on column
 #   for i in range(len(board)):
 #       situation.append(''.join(board2[i][:])) 

    #get info on lines
    for row in board2:
        situation.append(''.join(row))

    #get info on column
    for i in range(len(board2)):
        mycol=column(board2,i)
        situation.append(''.join(mycol))


    #diagonal, 2 possible situation
    situation.append(board2[0][0]+board2[1][1]+board2[2][2])
    situation.append(board2[2][0]+board2[1][1]+board2[0][2])

    if 'XXX' in situation:
        winner='X'
    elif 'OOO' in situation:
        winner='O'
    else:
        winner=EMPTY    

    if 'XXX' in situation and 'OOO' in situation:
        winner=EMPTY #this should be not possible!

    return winner    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True
    elif len(actions(board))==0:
        return True
    else:
        return False 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)=='X':
        return 1
    elif winner(board)=='O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board): #game end
        return None

    #potential_actions=actions(board)

    if player(board)=='X': #'X' want to maximize
     #   for action in potential_actions:
        Xval,move=Max_Value(board)
        #do enemy winning move so ennemy cant win
        # if Xval==-1:
        #     break
        # #if winning tested move, do it
        # if Xval==1:
        #     move=action
        #     break

    if player(board)=='O':
      #  for action in potential_actions:
        Oval,move=Min_Value(board)
        #do enemy winning move so ennemy cant win
        # if Oval==1:
        #     break
        # #if winning tested move, do it
        # if Oval==-1:
        #     move=action
        #     break

 #   print('minimax',Xval,move)
    return move

def Max_Value(board):
    val=  float('-inf')

    if terminal(board):
        return utility(board), None
    
   # print('hi')
  #  print('nexplayer is ', player(board))
    potential_actions=actions(board) #opponent potential actions
    #print(potential_actions)
    for action in potential_actions: 
      #  print('move:',action)        
        opp_board=result(board,action) #opponent action
      #  print('ennemy board:',opp_board)
        value,mov=Min_Value(opp_board) #opponent want to minimize
        #print(value,mov)
        if value>val:
            val=max(val,value)
            move=action #mov is ennemy 'minimizing' move!
        #this is maxplayer best move, no need to looks other actions
        if value==1:
            val=value
            move=action
           # print(value,mov,move)
            break    


    return val,move


def Min_Value(board):
    val=  float('inf')

    if terminal(board):
        return utility(board), None

    potential_actions=actions(board)
    for action in potential_actions:         
        opp_board=result(board,action) #opponent action
        value,mov=Max_Value(opp_board)
        if value<val:
            val=min(val,value)
            move=action
        #this is minplayer best move, no need to looks other actions
        if value==-1:
            val=value
            move=action
            break         

    return val,move
