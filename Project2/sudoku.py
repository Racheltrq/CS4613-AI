import math;
import copy;

class state:
	#class state has two attributes
	def __init__(self, lst, domain):
		self.lst = lst;          #lst contains the current sudoku
		self.domain = domain;	 #domain contains the current domains for all cells


	#check if there is any early failure
	#if there is black that only have one possible value on this branch, replace 0 by its value
	#update domain
	def forwardChecking(self):
		print("forwardChecking...");
		setForm(self.lst);


		for row in range(9):
			temp = set();
			for col in range(9):

				if self.lst[row][col] != "0":
					if self.lst[row][col] in temp:
						print("1111111111")
						return False;
					temp.add(self.lst[row][col]);
			for col in range(9):
				if self.lst[row][col] != "0":
					self.domain[row * 9 + col] = set();
				else:
					self.domain[row * 9 + col] -= temp;
					if len(self.domain[row * 9 + col]) == 0:
						print("2222222222", row, col)
						return False;


						
		for col in range(9):
			temp = set();
			for row in range(9):
				if self.lst[row][col] != "0":
					if self.lst[row][col] in temp:
						print("33333333")
						return False;
					temp.add(self.lst[row][col]);
			#print(temp);
			for row in range(9):
				if self.lst[row][col] != "0":
					self.domain[row * 9 + col] = set();
				else:
					self.domain[row * 9 + col] -= temp;
					if len(self.domain[row * 9 + col]) == 0:
						print("44444444")
						return False;

		#print("###", self.domain[38]);

		mul1 = 1;
		while(mul1 < 4):	
			mul2 = 1;
			while(mul2 < 4):
				temp = set();
				for row in range(3 * mul2 - 3, 3 * mul2):
					for col in range(3 * mul1 - 3, 3 * mul1):
						if self.lst[row][col] in temp and self.lst[row][col] != "0":
							print("555555555")
							print(row, col, self.lst[row][col], temp)
							return False;
						if self.lst[row][col] != "0":
							temp.add(self.lst[row][col]);
				for row in range(3 * mul2 - 3, 3 * mul2):
					for col in range(3 * mul1 - 3, 3 * mul1):
						if self.lst[row][col] != "0":
							self.domain[row * 9 + col] = set();
						else:
							self.domain[row * 9 + col] -= temp;
							if len(self.domain[row * 9 + col]) == 0:
								print("6666666")
								return False;						
				mul2 += 1;
			mul1 += 1;
		

		index = 0;
		setVal = 0;
		for item in self.domain:
			if len(item) == 1:
				row = int(math.floor(index / 9));
				col = index % 9;
				self.lst[row][col] = item.pop();
				print("111", row, col, "This block has only one possible value.");
				self.domain[index] = set();
				setVal = 1;
				break;
			index += 1;
		if setVal == 1:
			res = self.forwardChecking();
			if type(res) == list:
				return res;
		print("finishing forwardChecking...")
		if self.found() == True:
			#print("returning result")
			return self.lst;
		return True;



	#find the cell with lowest degree
	#return the index of it
	def lowerDegree(self, MRVindex):
		res = [];
		for index in MRVindex:
			i = index[0];
			j = index[1];
			count = 0;
			for m in range(9):
				if j != m and self.lst[i][m] == "0":
					count += 1;
			for n in range(9):
				if i != n and self.lst[n][j] == "0":
					count += 1;
			offset_i = i % 3;
			offset_j = j % 3;
			for m in range(i - offset_i, i - offset_i + 3):
				for n in range(j - offset_j, j - offset_j + 3):
					if m != i and n != j and self.lst[m][n] == "0":
						count += 1;
			res.append(count);
		lowestIndex = 0;
		lowestVal = res[0];
		for k in range(len(res)):
			if res[k] < lowestVal:
				lowestIndex = k;
				lowestVal = res[k];

		return lowestIndex;

	#find a list of index of possible next cell using MRV
	def nextCell(self):
		lowMRV = []; #store all the tuples of i,j values that have the lowest remaining value
		lowestLen = 0;
		for index in range(len(self.domain)):
			i = int(math.floor(index / 9));
			j = index % 9;
			if len(lowMRV) == 0 and self.lst[i][j] == "0":
				lowMRV = [(i, j)];
				lowestLen = len(self.domain[index]);
			elif self.lst[i][j] == "0" and len(self.domain[index]) < lowestLen:	
				lowMRV = [(i, j)];
				lowestLen = len(self.domain[index]);
			elif self.lst[i][j] == "0" and len(self.domain[index]) == lowestLen:
				if (i, j) not in lowMRV:
					lowMRV.append((i, j));
		indexCell = 0;
		print("lowestMRV", lowMRV)
		if len(lowMRV) > 1:
			indexCell = self.lowerDegree(lowMRV);

		return lowMRV[indexCell]

	#Check if the result is found
	def found(self):
		for i in self.lst:
			for j in i:
				if j == "0":
					return False;
		return True;


	#the backtraking algorithm
	def nextState(self):
		i = self.nextCell()[0];
		j = self.nextCell()[1];
		domain = self.domain[i * 9 + j];
		print(i, j, domain)
		state_temp = copy.deepcopy(self);
		res = state_temp.forwardChecking();
		if type(res) == list:
			print("NextState returning result...")
			return res;
		if res == False:
			return False;
		self.domain = copy.deepcopy(state_temp.domain);
		self.lst = copy.deepcopy(state_temp.lst);
		while len(domain) > 0:

			self.lst[i][j] = domain.pop();
			print("assume", i, j, "is", self.lst[i][j])
			
			
			state_temp = copy.deepcopy(self);
			res = state_temp.forwardChecking();
			if type(res) == list:
				print("NextState returning result...")
				return res;
			if res == False:
				print("forwardChecking failed.")
				self.lst[i][j] = "0";
			else:
				print(self.lst[i][j], "is not wrong");
				if state_temp.found() == True:
					print("RESULT FONUD!!!");
					setForm(state_temp.lst);
					return state_temp.lst;
				temp_nextState = state_temp.nextState();

					
				if type(temp_nextState) == list:
					print(setForm(temp_nextState))
					print("returning lst")
					print()
					return temp_nextState;

			print(i, j, "Keep guessing");

		

		if state_temp.forwardChecking() == False:
			print("here");
			print(i, j, domain);
			setForm(state_temp.lst);
			return False;



		
	#main search function
	#catch the return data from nextState
	def search(self):
		res = self.forwardChecking()
		if res == False:
			#print("first forwardChecking")
			return None;
		elif type(res) == list:
			print(res)
			return res;
		for i in self.domain:
			print(i)
		
		res = self.nextState();
		if type(res) == list:
			return res;
		else:
			return None;

		

		
#print the sudoku in 9 x 9 
def setForm(lst):
	for i in lst:
		print(" ".join(i));


#read file
def readin():
	sudoku_lst = [];
	print("Please enter the sudoku file name: ");
	filename = input();
	with open(filename) as file:
		for i in range(9):
			content = file.readline();
			content = content.split(" ");
			content[-1] = content[-1][:1];
			if "\n" in content:
				content.remove("\n");
			sudoku_lst.append(content);
	#setForm(sudoku_lst);
	file.close();
	return sudoku_lst;





def main():
	recursion = 0;
	sudoku_lst = readin();
	domain = [];
	for i in range(81):
		domain.append({"1", "2", "3", "4", "5", "6", "7", "8", "9"});
	state_new = state(sudoku_lst, domain);

	res = state_new.search();
	f = open("Output3", "w+"); #change your output file name
	if res == None:
		f.write(None);
	else:
		for i in res:
			f.write(" ".join(i));
			f.write("\n");
	f.close();

main();















	