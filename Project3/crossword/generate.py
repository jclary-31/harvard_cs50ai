import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """

        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for domain in self.domains.keys():            
            words=self.domains[domain].copy()
            for word in words:
                if len(word)!=domain.length:
                    self.domains[domain].remove(word)
        #    print(node,self.domains[node])   

          

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised=False
        #print(self.crossword.overlaps[x,y])
        print(self.domains[x])
        #print(self.domains[y])
        index=self.crossword.overlaps[x,y]
        if index is not None:
            tokeep=set()
            for wordx in self.domains[x]:
                for wordy in self.domains[y]:
                    if wordx[index[0]]==wordy[index[1]]:
                        tokeep.add(wordx)
            
            if self.domains[x]==tokeep:#this is the 2nd time revision is done +same results
                revised=False
            else:                
                self.domains[x]=tokeep
                revised=True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None or arcs==[]:
            arcs=[]
            alldomains=list(self.domains.keys())
            for domain1 in alldomains:
                for domain2 in alldomains:
                    if domain1 !=domain2:
                        arcs.append((domain1,domain2))  
        queue=arcs.copy()

       # i=1
        while len(queue)>0:
            #i=i+1
            #print(i,queue)
            x,y =list(queue)[-1]#last come first serve, to follow consequence chain of modif
            queue.remove((x,y))
            #print(x,'vs',y)
            if self.revise(x,y): #revise give true IF x and y overlap
                if len(self.domains[x])==0:
                    return False
                for domain in (self.crossword.neighbors(x)-{y}):
                    queue.append((domain,x))
                        #print(x,'|',y,' || ',domain)
        return True           

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for domain in self.domains:
            if domain not in assignment:
                return False
        return True #this happens only if all domains are filled
         
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # all values are distinct,`
        # #set return unique elements so if len(set()) is same as len(list), then values are unique
        if len(list(assignment.values()))!= len(set(assignment.values())): 
            return False
            

        for domain in assignment:
            word=assignment[domain]

            #  every value is the correct length,
            if len(word)!=domain.length:
                return False

            #  and there are no conflicts between neighboring variables.
            neighbors=self.crossword.neighbors(domain)
            for neighb in neighbors:
                if neighb in assignment:
                    neighb_word=assignment[neighb]
                    index=self.crossword.overlaps[domain,neighb]
#                    print(word)
 #                   print(neighb_word)
                    if word[index[0]]!=neighb_word[index[1]]:
                        return False

        return True        
                    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #idea is to get the less contraining choice for a given domain

        toignore=assignment.keys() #to not be counted in 
        neighbors=self.crossword.neighbors(var)

        mydic=dict()
        for word in self.domains[var]:
            n=0
            for neighb in (neighbors - toignore):
                for neighb_word in self.domains[neighb]:
                    index=self.crossword.overlaps[var,neighb]
                    if word[index[0]]!=neighb_word[index[1]] :#word NOT consistent with
                        n=n+1
            mydic[word]=n

        out=sorted(mydic,key=mydic.get)
        return out


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
      #  print(self.domains)
        freedomains= list(self.domains.keys()- assignment.keys() )

        alist=[]
        for domain in freedomains:
            words=self.domains[domain]
            nwords=len(words)
            alist.append((domain,words,nwords))

        alist.sort(key=lambda x: x[2])
        # print(alist)

        #somethingwrong here with check50 
        # select_unassigned_variable doesn't choose a variable if already assigned
        #??????
        #  if len(alist)>1:
        #     if alist[0][2]==alist[1][2]:#if the first two have same number of word, to recode with while?
        #         a1=self.crossword.neighbors(alist[0][0])
        #         a2=self.crossword.neighbors(alist[1][0])
        #         degrees=[ ( alist[0][0],len(a1) ),  ( alist[1][0], len(a2) )]#numbre of neghbors
        #         degrees.sort(key=lambda x: x[1])
        #         # print('degree',degrees)
        #         domain=degrees[-1][0]#last one has the higher degrees (number of connexion)
        # else:
        domain=alist[0][0]#minimum number of remaining values

        #print('unassigned', domain)
        return domain    

    def inference(self,domain):
        """
        Enforce arc consistency from a domain with consistent assignement to the neighbors

        """

        arcs=[]
        for neighb in self.crossword.neighbors(domain):
            arcs.append((domain,neighb))

        self.ac3(arcs)


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment
        
        domain = self.select_unassigned_variable(assignment)# choose a domain not in assignment
        #print(self.domains)
        for word in self.order_domain_values(domain,assignment):
            new_assign=assignment.copy()
            new_assign[domain]=word
            #print(domain,'|',word)           

            if self.consistent(new_assign):
                self.inference(domain)# use ac3 and revise, which update self.domains[x]=tokeep
                result=self.backtrack(new_assign)
                
                if result is not None:
                    return result
                
                del new_assign[domain] #if result=none; added assignement if not good
        return None





def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
