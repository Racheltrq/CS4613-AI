import copy;

initialState = [[0 for i in range(3)] for j in range(3)];
goalState = [[0 for i in range(3)] for j in range(3)];
queue = [];
prevNodes = [];
total = 1;

#each state is represented by a class
class state:
    def __init__(self, array, path_prevNodes, prevActions, cost, heur):
        self.array = array;     #the matrix in current node
        self.path_prevNodes = path_prevNodes;       #previous node above it
        self.prevActions = prevActions;
        self.cost = cost;
        self.heur = heur;

#generate the next node
def generateChildren(expandNode, newArray, cost, action, mode):
    newPrevNodes = expandNode.path_prevNodes;
    newPrevNodes.append(expandNode);
    newPrevActions = copy.deepcopy(expandNode.prevActions);
    newPrevActions.append(action);
    newState = state(newArray, newPrevNodes, newPrevActions, cost + 1, heuristic(mode, newArray));
    return newState;

#expand the current node
def next(queue, mode, total):
    expandNode = queue.pop(0);

    i, j = pos(expandNode.array);


    if i < 2:
        temp = copy.deepcopy(expandNode.array);
        newArray = up(i, j, temp);
        if newArray not in prevNodes:
            copy_expandNode = copy.deepcopy(expandNode);
            newState = generateChildren(copy_expandNode, newArray, expandNode.cost, 'D', mode);
            queue.append(newState);
            prevNodes.append(newState.array);
            total += 1;

    if i > 0:
        temp = copy.deepcopy(expandNode.array);
        newArray = down(i, j, temp);
        if newArray not in prevNodes:
            #print("newArray:", newArray);
            copy_expandNode = copy.deepcopy(expandNode);
            newState = generateChildren(copy_expandNode, newArray, expandNode.cost, 'U', mode);
            queue.append(newState);
            prevNodes.append(newState.array);
            total += 1;

    if j < 2:
        temp = copy.deepcopy(expandNode.array);
        newArray = left(i, j, temp);
        if newArray not in prevNodes:
            #print("newArray:", newArray);
            copy_expandNode = copy.deepcopy(expandNode);
            newState = generateChildren(copy_expandNode, newArray, expandNode.cost, 'R', mode);
            queue.append(newState);
            prevNodes.append(newState.array);
            total += 1;

    if j > 0:
        temp = copy.deepcopy(expandNode.array);
        newArray = right(i, j, temp);
        if newArray not in prevNodes:
            #print("newArray:", newArray);
            copy_expandNode = copy.deepcopy(expandNode);
            newState = generateChildren(copy_expandNode, newArray, expandNode.cost, 'L', mode);
            queue.append(newState);
            prevNodes.append(newState.array);
            total += 1;
    return total;


#determine the position of 0
def pos(array):
    for i in range(3):
        for j in range(3):
            if array[i][j] == '0':
                return i, j;

#move down
def up(i, j, array):
    #print('up');
    array[i][j] = array[i + 1][j];
    array[i + 1][j] = '0';
    return array;

#move up
def down(i, j, array):
    #print('down');
    array[i][j] = array[i - 1][j];
    array[i - 1][j] = '0';
    return array;

#move right
def left(i, j, array):
    #print('left');
    array[i][j] = array[i][j + 1];
    array[i][j + 1] = '0';
    return array;

#move left
def right(i, j, array):
    #print('right');
    array[i][j] = array[i][j - 1];
    array[i][j - 1] = '0';
    return array;




def readfile(file_name):
    with open(file_name) as fn:
        lines = [line.rstrip('\n') for line in open(file_name)];
    for i in range(7):
        if i < 3:
            initialState[i] = [lines[i][:1], lines[i][2:3], lines[i][4:]];
        elif i > 3:
            goalState[i-4] = [lines[i][:1], lines[i][2:3], lines [i][4:]];
    #print("initialState:", initialState);
    #print("goalState:", goalState);

def sumManhattan(currentArray):
    init_i = init_j = goal_m = goal_n = sum = 0;
    while init_i < 3:
        init_j = 0;
        while init_j < 3:
            temp = currentArray[init_i][init_j];
            if temp != '0':
                for goal_m in range(3):
                    for goal_n in range(3):
                        if temp == goalState[goal_m][goal_n]:
                            sum = sum + abs(init_i - goal_m) + abs(init_j - goal_n);
                            #print(init_i, init_j, goal_m, goal_n);
                            #print('sum:', sum);
            init_j += 1;
        init_i += 1;
    return sum;


def linearConlict(currentArray):
    count = 0;

    init_col = [[], [], []];
    goal_col = [[], [], []];
    for i in range(3):
        for j in range(3):
            init_col[i].append(currentArray[j][i]);
            goal_col[i].append(goalState[j][i]);

    for i in range(3):
        count += countReverse(currentArray[i], goalState[i]);
        count += countReverse(init_col[i], goal_col[i]);
    return count;

#count numbers that are in reverse order in one line
def countReverse(lst1, lst2):
    num_same = 0;
    index_array = []
    count = 0;
    for i in lst1:
        if i in lst2:
            if i != '0':
                num_same += 1;
    if num_same <= 1:
        return 0;
    else:
        for i in range(3):
            for j in range(3):
                if lst1[i] == lst2[j] and lst1[i] != '0':
                    index_array.append(i);
                    index_array.append(j);
        if num_same == 2:
            if (index_array[0] < index_array[2]) and (index_array[1] > index_array[3]):
                count += 1;
        else:
            if (index_array[0] < index_array[2]) and (index_array[1] > index_array[3]):
                count += 1;
            if (index_array[2] < index_array[4]) and (index_array[3] > index_array[5]):
                count += 1;
            if (index_array[0] < index_array[2]) and (index_array[3] > index_array[5]):
                count += 1;
    return count;

#switch mode here
def heuristic(mode, array):
    if mode == 'M':
        return sumManhattan(array);
    elif mode == 'L':
        return sumManhattan(array) + 2 * linearConlict(array);


def main():
    print("Please enter the name of the input file:");
    file_name = input();
    print("Please enter the name of the output file:");
    outputFileName = input();
    readfile(file_name);
    print("Please choose your heuristic function:\nManhattan distance(M) Manhattan distance+2*LinearConlict(L):");
    mode = input();
    sumMan = sumManhattan(initialState);
    outputFile = open(outputFileName, "w");

    for i in initialState:
        outputFile.write(' '.join(i));
        print(' '.join(i));
        outputFile.write("\n");
    outputFile.write("\n");
    print();
    for i in goalState:
        outputFile.write(' '.join(i));
        print(' '.join(i));
        outputFile.write("\n");
    outputFile.write("\n");
    print();

    currentArray = copy.deepcopy(initialState);
    currentState = state(currentArray, [], [], 0, heuristic(mode, currentArray));
    queue.append(currentState);

    numNodes = next(queue, mode, total);
    queue.sort(key = lambda x: x.cost + x.heur);

    while queue[0].array != goalState:
        numNodes = next(queue, mode, numNodes);
        queue.sort(key = lambda x: x.cost + x.heur);

    resNode = queue[0];
    outputFile.write(str(resNode.cost));
    outputFile.write("\n");
    outputFile.write(str(len(prevNodes)));
    outputFile.write("\n");
    outputFile.write(' '.join(resNode.prevActions));
    print(resNode.cost);
    print(len(prevNodes));
    print(' '.join(resNode.prevActions));
    lst = [];
    for i in resNode.path_prevNodes:
        #print(i.cost, i.heur);
        lst.append(str(i.heur + i.cost));
    outputFile.write("\n");
    outputFile.write(' '.join(lst))
    outputFile.close();

    print(' '.join(lst));


main();
