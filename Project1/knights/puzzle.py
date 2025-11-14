from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

theword=And(
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    Or(BKnight,BKnave),
    Not(And(BKnight,BKnave)),
    Or(CKnight,CKnave),
    Not(And(CKnight,CKnave))
)

# Puzzle 0
# A says "I am both a knight and a knave."
#A cant be both->  A lie-> A is a knave
Asentence=And(AKnight,AKnave)

knowledge0 = And(
    theword,
    Implication(AKnight,Asentence)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
#Aknave + Bknave -> A true  -> Aknight !=Aknave_hypothesis
#Aknave + Bknight -> A lie  -> Aknave ok +learn Bknight
#Aknight +        -> A true -> Aknight!= Aknave_hypothesis
Asentence=And(AKnave,BKnave)

knowledge1 = And(
    theword,
    Implication(AKnight,Asentence),
    Implication(AKnave,Not(Asentence)) #if Aknave then he lie, test this
#    Implication(BKnight,Asentence), #useless
#    Implication(BKnave,Asentence)  #useless
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Asentence=Or(And(AKnight,BKnight),And(AKnave,BKnave))
Bsentence=Or(And(AKnight,BKnave),And(AKnave,BKnight))

knowledge2 = And(
    theword,
    Implication(AKnight,Asentence),
    Implication(AKnave,Not(Asentence)),
    Implication(BKnight,Bsentence),
    Implication(BKnave,Not(Bsentence))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Asentence=Or(AKnight,AKnave)
Bsentence1a= Implication(AKnight,BKnave)# if bknight
Bsentence1b= Implication(AKnave,Not(BKnave))#if bknave
Bsentence2=CKnave
Csentence= AKnight  

knowledge3 = And(
    theword,
    Implication(AKnight,Asentence),
    Implication(AKnave,Not(Asentence)),
    Implication(BKnight,Bsentence1a),
    Implication(BKnave,Bsentence1b),
    Implication(BKnight,Bsentence2),
    Implication(BKnave,Not(Bsentence2)),
    Implication(CKnight,Csentence),
    Implication(CKnave,Not(Csentence))    
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
