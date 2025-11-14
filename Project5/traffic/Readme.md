
# A quick description on  the tests for german traffic panels recognition


## setup 0 (initial): a sequential model with
    - a 2d convolutional layer ; 10 filters with 3*3 kernel ; and relu activation
    - a max pooling layer using a 2*2
    - a flatten step (input for the NN)
    - a hidden layer with 64 nodes and relu activation
    - no dropout
    - ouput layer have softmax activation

## setup 1
    - setup 0
    - + 20% dropout on the hidden layer

## setup 2
    - setup 0
    -  + 20% dropout on input data (i.e. before convolution layer)

## setup 3
    - setup 0 
    - + 20 filter in conv layer

## setup 4
    - setup 0 
    - but sigmoid activation in the hidden layer

## setup 5
    - setup 0
    - but hidden layer, one with relu and one with sigmoid activation. each have 32 nodes


# some results (metrics on test set)
        | accuracy  | loss    
setup 0 |   0.94    | 0.18
setup 1 |   0.95    | 0.18   
setup 2 |   0.90    | 0.43
setup 3 |   0.96    | 0.18
setup 4 |   0.97    | 0.13
setup 5 |   0.91    | 0.38



# moral
 - adding dropout at the beginning (i.e. on data) is counterproductive
 - adding a hidden layer (while same total number of hidden nodes) increase loss

# notes
in setup 0 and 1, loss change from 0.15 to 0.26 from one runs to another (without changing the setup)

