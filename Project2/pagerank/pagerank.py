import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    #corpus={"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    #print('corpus',corpus)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    #modify the corpus so if a webpage with no outgoing links
    # is has if links with every page (includind itself)
    for apage in corpus.keys():
        if corpus[apage]==set():
            corpus[apage]=set(corpus.keys())
                
#    #create the table for related links
#    links_inpage=corpus.get(page)
#    N=len(links_inpage)
#    mydic=dict()
#    for akey in links_inpage:
#        mydic[akey]=damping_factor/N

    allkeys=corpus.keys()
    links_inpage=corpus.get(page)

    Nlinks=len(links_inpage)
    N=len(allkeys)

    Transition=dict()
    for apage in allkeys:
        if apage in links_inpage:
            Transition[apage]=damping_factor/Nlinks+(1-damping_factor)/N
        else:
            Transition[apage]=(1-damping_factor)/N    

    #check if sum(values)==1?


    return Transition


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #I want dict(page:rank%)

    allpages=corpus.keys()
    visited=[]

    i=0
    while i<n:
        if i==0:
            page= random.choice(list(allpages))
        else:
            page=random.choices(population=pagelist,weights=chances)[0] 
 
        visited.append(page)

        transition=transition_model(corpus,page,damping_factor)
        pagelist=list(transition.keys())
        chances=list(transition.values())

#        if i<4:
#            print('transition',transition)
#            print(sum(chances))# =1 at each iteration; ok

        i=i+1

    #count n time a given page is visited and normalize
    Pagerank=dict()
    for page in allpages:
        rank=0
        for pag in visited:
            if page==pag:
                rank=rank+1
        Pagerank[page]=rank/len(visited)        
    

    return Pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # calculate a page’s PageRank based on the PageRanks of all pages that link to it). 

    allpages=corpus.keys()

    #initial state
    Pagerank=dict()
    for pag in allpages:     
        Pagerank[pag]=1/len(allpages)


    acc=1e3 #
    while acc>0.001:

 #   print('corpus',corpus)
 #   print('rank',Pagerank)
#    page=random.choice(list(allpages))

        parents=dict()
        for linked in allpages:
            ranks=[]
            for source in allpages:
                if linked in corpus[source]:
                    #print(linked,corpus[source],Pagerank[source])
                    ranks.append(Pagerank[source]/len(corpus[source]))

            if len(ranks)==0:# page is not referenced anywhere
                ranks=[0]#or ?[1/len(allpages)]
            parents[linked]=ranks

        #print('parent rank',parents)
        PR_child=dict()
        for page in allpages:
            PR_child[page]=(1-damping_factor)/len(allpages)\
                        +damping_factor*sum(parents[page])

        #normalize child
        norm=sum(PR_child.values())
        for page in allpages:
            PR_child[page]=PR_child[page]/norm

        #print('parents',Pagerank)
        #print('cchild',PR_child)
        #compute error on Pageranks vs child
        err=[]
        for page in allpages:
            dif=abs(Pagerank[page]-PR_child[page])
            err.append(dif)
        acc=sum(err)

        #print(acc)

        #update Pagerank
        Pagerank=PR_child

    return Pagerank    


if __name__ == "__main__":
    main()
