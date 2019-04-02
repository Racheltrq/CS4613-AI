initialState = [[0 for i in range(3)] for j in range(3)];
goalState = [[0 for i in range(3)] for j in range(3)];


def readfile(file_name):
    with open(file_name) as fn:
        lines = [line.rstrip('\n') for line in open(file_name)];
    for i in range(7):
        if i < 3:
            initialState[i] = [lines[i][:1], lines[i][2:3], lines[i][4:]];
        elif i > 3:
            goalState[i-4] = [lines[i][:1], lines[i][2:3], lines[i][4:]];

    print("initialState:", initialState);
    print("goalState:", goalState);

def sumManhattan():
    pass

def linearConlict():
    pass




def main():
    print("Please enter the name of the input file");
    #file_name = input();
    file_name = 'input.txt';
    readfile(file_name);
    #print();

main();
