import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        #see https://cs50.harvard.edu/ai/2024/projects/1/minesweeper/ figure1
        if len(self.cells)==self.count and self.count!=0:
            #print('known mines: ', self.cells)
            return self.cells
        else:
            return set()


    def known_safes(self): 
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #this is the 'opposite' of known_mine
        if self.count==0:
            #print('safe mines: ', self.cells)
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #if {A, B, C} = 2 and C=mine then new sentence is {A,B}=1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count=self.count-1 

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #if {A, B, C} = 2 and C=safe then new sentence is {A,B}=2
        if cell in self.cells:
            self.cells.remove(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        #print('mine', self.mines)
        #print('(i,j)', cell)
        
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)#Updates internal knowledge 

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        #print('safe', self.safes)
        #print('(i,j)', cell)
        
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)#Updates internal knowledge
            #print(sentence) 

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        

        #2) mark the cell as safe (cell is played but I don't lost)
        #add to self.safe and update sentence in knowledge
        self.mark_safe(cell) 


        #3) add a new sentence to the AI's knowledge base
        #based on the value of `cell` and `count`

        #this is similar to Minesweeper.nearby_mines 
        #but adapted to knowledge sentence, where sentence is {A,B,C}=number
        # suppose a lign ABC and {B}=1 then {A,C}=1 (condidering A and C not known)

        #suppose a lign ABC and {B}=1 then {A,C}=1 
        #  and alsosuppose A is known and A=safe, then C=1 ; nothing to change (not sure)
        #  or also suppose A is known and A=mine, then C=safe=0=1-1 ;decrease count by 1 eachtime

        neigbors=set() #stack available neigbors here
        # Loop over all cells within one row and column, see in Minesweeper.nearby_mine
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if 0 <= i < self.height and 0 <= j < self.width: # this is for domain limits
                
                    if (i, j) != cell:#we look around (i,j)=cell
                        if (i,j) not in self.safes:
                            if(i,j) not in self.mines:
                                neigbors.add((i,j))
                            if (i,j) in self.mines:
                                count=count-1    

        #problem here if sentence={(7, 4), (5, 5), (7, 6), (7, 5), (6, 6), (5, 4), (6, 4)} = 2
        #and i play (6, 4)
        #knowledge became      {(7, 4), (5, 5), (7, 6), (7, 5), (6, 6), (5, 4)} = 2
        # if (7,4)=bomb then  {(5, 5), (7, 5), (5, 4), (6, 3), (7, 3)} = 1
        # when count become count -1 ; previous statement need to be removed!! done in mark.mine later

        newsentence=Sentence(neigbors,count)

        #for sent in self.knowledge:        
        #    print('alreadyknown',sent)
        #print('newsentence',newsentence)
        

        #print(' new sentence:', newsentence, '\n around cell',cell)
        if len(neigbors)!=0 and newsentence not in self.knowledge:
            self.knowledge.append(newsentence)



        #i found some empty set() in sentence
        for sentence in self.knowledge:#could be on new knowledge only?
            if len(sentence.cells)==0: # mark_safe and mark_mine : the cell is removed from sentence once treated!
                self.knowledge.remove(sentence)
        

        ###################NEED A RECURSIVE INFERING operation here

        exist_changes=True
        #4) mark any additional cells as safe or as mines
        #if it can be concluded based on the AI's knowledge base
        # -> add to self.safe or self.mine and update sentence in knowledge
        # -> need identify both case 
        #self.mark safe call sentence.mark_safe for all sentences in KB
        # and add given cell to safes
        #sentence.mark_safe remove the cell from sentence
        #I=0
        while exist_changes:
            #print('ROUND',I)
            #I=I+1
            exist_changes=False

            for sentence in self.knowledge:
                if len(sentence.cells)>1: # mark_safe and mark_mine : the cell is removed from sentence once treated!
                    #if sentence.count==0:
                    for cell in list(sentence.known_safes()):
                        self.mark_safe(cell)
                        exist_changes=True
                        #print('safe cell',cell)

                #if sentence.count==len(sentence.cells) and sentence.count!=0:
                for cell in list(sentence.known_mines()):  
                    for cell in list(sentence.cells):
                        self.mark_mine(cell)
                        exist_changes=True



            #print('all played moves:',self.moves_made)
            #print('all mines:',self.mines)
            #print('all safe move:',self.safes-self.moves_made)#safes some of contain moves_made

            #i found some empty set() in sentence
            for sentence in self.knowledge:
                if len(sentence.cells)==0: # mark_safe and mark_mine : the cell is removed from sentence once treated!
                    self.knowledge.remove(sentence)
                    exist_changes=True

        #5) add any new sentences to the AI's knowledge base
        #if they can be inferred from existing knowledge
        
        ### set1-set2 is not set2-set1!!!  see numpy function setdiff1d
        #set1-set2 : what is in set1 BUT NOT in set2
        # set2-set1 : in set2 but not in set1
        #set1.intersec(set1,set2) : common elements in set1 and in set2
        # make a double  loop and dont keep empty case (where cell=set())

 #       print(self.knowledge)
            for sentence1 in self.knowledge:
    #           print('sentence is:',sentence1)
                for sentence2 in self.knowledge:
                    if (len(sentence1.cells)!=0 and len(sentence2.cells)!=0 and# non empty sentence
                        sentence1.cells!=sentence2.cells and #twice the same info is useless
                        #set(sentence1.cells).intersection(sentence1.cells,sentence2.cells)!=set() #sentence 1 and 2 must share something
                        set(sentence1.cells).issuperset(sentence2.cells)# intersection not good, in fact one set is in another or no infer
                        ):
                        #print('fusion')
                        inferred_cell=sentence1.cells-sentence2.cells #should be ok as sentence1=the_superset
                        #inferred_cell=set(sentence1.cells).intersection(sentence1.cells,sentence2.cells) 
                        inferred_count=sentence1.count-sentence2.count
                        #print('in',inferred_cell)
                        if len(inferred_cell)>0 and inferred_count>=0:
                            phrase=Sentence(inferred_cell,inferred_count)
                            #print('inferred',phrase)
                            if phrase not in self.knowledge:
                                #print('sentence1:', sentence1)
                                #print('sentence2:', sentence2)
                                #print('sentence to add to knowledge',phrase)
                                self.knowledge.append(phrase)
                                exist_changes=True

            # print('changes',exist_changes)
           
            #print('safes2play',self.safes-self.moves_made)
            #print('mines',self.mines)



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # safes contain some of move_mades!!!!!!
        candidates=[]
        for move in self.safes:
            if move not in self.moves_made:
                candidates.append(move)
        
        if len(candidates)==0:
            return None
        else:
            #print('good choice:',candidates)
            return random.choice(list(candidates))
                

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        possiblechoice=set()

        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    possiblechoice.add((i,j))


        #take one randomly in possiblechoice
        move=random.choice(list(possiblechoice)) 

        return  move        