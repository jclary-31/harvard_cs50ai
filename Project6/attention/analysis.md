# Analysis

## Layer 4, Head 10

This head pays attention to the words surrounding the mask (here an adjective). It also pays attention to CLS token.

Example Sentences:
- Artificial Intelligence leads to [MASK] stupidity.
- He was kind of lazy and avoid [MASK] tasks.

## Layer2, Head 7

This head pays attention to the names around the unknown action verb. In First sentence, mask is in relationship with the CLS, whereas it is not in the 2nd sentence.

Example Sentences:
- The cat [MASK] on the sofa.
- She [MASK] orange and bananas at the store.

## Layer2, Head 2

This head pays attention to the next word in the sentence. Here mask is a noun. In second sentence, word 'situation' have no attention

- Once upon a time, there was a beautiful [MASK] kept by a dragon.
- He founded himself in a tricky situation as [MASK] was too hard in all cases.
