import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    data=[]
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)


    tointeger=['Administrative',
            'Informational',
            'ProductRelated',
            'OperatingSystems',
            'Browser',
            'Region',
            'TrafficType'
            ]


    tofloat=['Administrative_Duration',
            'Informational_Duration',
            'ProductRelated_Duration',
            'BounceRates',
            'ExitRates',
            'PageValues',
            'SpecialDay'
            ]

    #-Month, an index from 0 (January) to 11 (December)
    months=['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec']
    months_values=[0,1,2,3,4,5,6,7,8,9,10,11]
    Month_dic=dict(zip(months,months_values))

    #- VisitorType, an integer 0 (not returning) or 1 (returning)
    VisitType=['Returning_Visitor','New_Visitor','Other']
    VisitType_value=[1,0,0]
    Visit_dic=dict(zip(VisitType,VisitType_value))

    #- Weekend, an integer 0 (if false) or 1 (if true)
    isweekend=['TRUE','FALSE']
    isweekend_value=[1,0]
    WE_dic=dict(zip(isweekend,isweekend_value))

    #revenue
    isrevenue=['TRUE','FALSE']
    isrevenue_value=[1,0]
    Rev_dic=dict(zip(isrevenue,isrevenue_value))

    evidence=[]
    labels=[]
    for dic in data:
        for key in dic.keys():
            if key in tointeger:
                dic[key]=int(dic[key])
            elif key in tofloat:
                dic[key]=float(dic[key])
            elif key=='Month':
                dic[key]=Month_dic[dic[key]]
            elif key=='VisitorType':
                dic[key]=Visit_dic[dic[key]]
            elif key=='Weekend':
                dic[key]=WE_dic[dic[key]]
            elif key=='Revenue':
                dic[key]=Rev_dic[dic[key]]
        labels.append(dic.pop('Revenue'))        
        evidence.append(list(dic.values()))                   

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    model=KNeighborsClassifier(weights='distance',n_neighbors=1)
    model.fit(evidence,labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    npredic_true=0
    npredic_false=0
    norm_true=0
    norm_false=0
    for i in range(len(labels)):
        if labels[i]==1:
            norm_true=norm_true+1
            if predictions[i]==1:
                npredic_true=npredic_true+1
        if labels[i]==0:
            norm_false=norm_false+1 
            if predictions[i]==0:    
                npredic_false=npredic_false+1
    
    sensitivity=npredic_true/norm_true
    specificity=npredic_false/norm_false

    
    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
