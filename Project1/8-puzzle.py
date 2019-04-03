initialState = [[0 for i in range(3)] for j in range(3)];
goalState = [[0 for i in range(3)] for j in range(3)];

class state:
    def __init__(self, array, cost, heur):
        self.array = array;
        self.cost = cost;
        self.heur = heur;

    def next(self):



def readfile(file_name):
    with open(file_name) as fn:
        lines = [line.rstrip('\n') for line in open(file_name)];
    for i in range(7):
        if i < 3:
            initialState[i] = [lines[i][:1], lines[i][2:3], lines[i][4:]];
        elif i > 3:
            goalState[i-4] = [lines[i][:1], lines[i][2:3], lines [i][4:]];

    print("initialState:", initialState);
    print("goalState:", goalState);

def sumManhattan():
    init_i = init_j = goal_m = goal_n = sum = 0;
    while init_i < 3:
        init_j = 0;
        while init_j < 3:
            temp = initialState[init_i][init_j];
            if temp != '':
                for goal_m in range(3):
                    for goal_n in range(3):
                        if temp == goalState[goal_m][goal_n]:
                            sum = sum + abs(init_i + init_j - goal_m - goal_n);
                            #print(init_i, init_j, goal_m, goal_n);
                            #print('sum:', sum);
            init_j += 1;
        init_i += 1;
    return sum;



def linearConlict():
    count = 0;

    init_col = [[], [], []];
    goal_col = [[], [], []];
    for i in range(3):
        for j in range(3):
            init_col[i].append(initialState[j][i]);
            goal_col[i].append(goalState[j][i]);

    for i in range(3):
        count += countReverse(initialState[i], goalState[i]);
        count += countReverse(init_col[i], goal_col[i]);
    print("linearConlict:", count);



def countReverse(lst1, lst2):
    num_same = 0;
    index_array = []
    count = 0;
    for i in lst1:
        if i in lst2:
            if i != ' ':
                num_same += 1;
    if num_same <= 1:
        return 0;
    else:
        for i in range(3):
            for j in range(3):
                if lst1[i] == lst2[j] and lst1[i] != ' ':
                    index_array.append(i);
                    index_array.append(j);
        if num_same == 2:
            if index_array[3] < index_array[1]:
                count += 1;
        else:
            if index_array[3] < index_array[1]:
                count += 1;
            if index_array[5] < index_array[1]:
                count += 1;
            if index_array[5] < index_array[3]:
                count += 1;
    return count;





def main():
    print("Please enter the name of the input file");
    #file_name = input();
    file_name = 'input.txt';
    readfile(file_name);
    sumMan = sumManhattan();
    print('ManSum:', sumMan);
    linearConlict();
    #print();

main();
