import nltk
import sys
import re

#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger_eng')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | NP VP P NP VP
AP -> A | A AP
NP -> N | Det NP | AP NP | NP PP | Adj NP | NP Adv
PP -> P | P NP 
VP -> V | V NP | VP PP |Adv VP |VP Adv | VP Conj VP
"""

#Holmes sat down and lit his pipe.

# NONTERMINALS = """
# S -> NP VP | NP VP Conj NP VP | NP VP P NP VP
# VP -> V | V NP | V PP | Adv VP | VP Adv | VP  Conj VP
# NP -> N | Det NP | AP NP | N PP | Conj NP | NP Adv | Adj NP
# AP -> Adj | Adj AP | Adv AP
# PP -> P NP
# """
#N V P Det Adj N# Det N V
#N V Adv Conj V Det N

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
        #print(trees)
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    ##remove some structural characters
    sentence=sentence.replace('.','')
    sentence=sentence.replace(',','')
    sentence=sentence.replace('?','')
    sentence=sentence.replace('!','')
    sentence=sentence.replace(':','')


    sentence=sentence.split()

    text=[]
    for word in sentence:
        if word.isalpha():
            text.append(word.lower())

    phrase=' '.join(text)

    token=nltk.tokenize.word_tokenize(phrase)
    #print('tokens=',token)

    return  token


    # test = re.compile('[a-zA-Z]')

    # # Tokenize using nltk:
    # tokens = nltk.word_tokenize(sentence)

    # # Return list of lowercase strings that match Regex:
    # return [entry.lower() for entry in tokens if test.match(entry)]



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
#    print(tree.subtrees())
    alist=[]
    for subtree in tree.subtrees():   
        if subtree.label()=='NP' :#and len(subtree)==1:
            ntag_N=0
            for leave in subtree.pos():
                (expression, tag) = leave
                if tag=='N':
                    ntag_N=ntag_N+1
            if ntag_N<2:
                alist.append(subtree)
            
    return alist

if __name__ == "__main__":
    main()
