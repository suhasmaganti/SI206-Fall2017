import os
import filecmp
import csv
from collections import OrderedDict
import operator
from datetime import datetime

def getData(file):
#Input: file name
#Ouput: return a list of dictionary objects where 
#the keys will come from the first row in the data.

#Note: The column headings will not change from the 
#test cases below, but the the data itself will 
#change (contents and size) in the different test 
#cases.

	#Your code here:

	with open(file) as f:
		list_dic = [{k: i for k, i in row.items()}
			for row in csv.DictReader(f, skipinitialspace=True)]
	return list_dic
	
#Sort based on key/column
def mySort(data,col):
#Input: list of dictionaries
#Output: Return a string of the form firstName lastName

	#Your code here:

	if col == "First":
		sorted_data = sorted(data, key = lambda x: x["First"])
		return sorted_data[0][col] +' '+ sorted_data[0]["Last"]
	elif col == "Last":
		sorted_data = sorted(data, key = lambda x: x["Last"])
		return sorted_data[0]["First"] +' '+ sorted_data[0][col]
	else:
		sorted_data = sorted(data, key = lambda x: x["Email"])
		return sorted_data[0]["First"] +' '+ sorted_data[0]["Last"]
	

#Create a histogram
def classSizes(data):
# Input: list of dictionaries
# Output: Return a list of tuples ordered by
# ClassName and Class size, e.g 
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]

	#Your code here:
	fresh = 0
	soph = 0
	jr = 0
	sr = 0

	dic = {"Freshman" : fresh, "Sophomore" : soph, "Junior" : jr, "Senior" : sr}

	for x in data:
		if x["Class"] == "Freshman":
			dic["Freshman"] += 1
		elif x["Class"] == "Sophomore":
			dic["Sophomore"] += 1
		if x["Class"] == "Junior":
			dic["Junior"] += 1
		if x["Class"] == "Senior":
			dic["Senior"] += 1

	a = sorted(dic.items(), key=operator.itemgetter(1), reverse = True)
	return a


# Find the most common day of the year to be born
def findDay(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB

	#Your code here:
	pop_day_count = {}
	for i in a:
		bday = i["DOB"]
		day = bday.split('/')
		d = day[1]

		if d not in pop_day_count:
			pop_day_count[d] = 1
		else:
			pop_day_count[d] += 1

	sort_pop_day = sorted(pop_day_count.items(), key = operator.itemgetter(1), reverse = True)
	return(int(sort_pop_day[0][0]))


# Find the average age (rounded) of the Students
def findAge(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB
	
	#Your code here:
	mean = 0
	count = 0

	for i in a:
		bday = i["DOB"]
		b_date = bday.split('/')
		
		d = datetime.today()
		today = d.strftime('%d/%m/%Y')
		day = today.split('/')

		b_date = list(map(int, b_date))
		day = list(map(int, day))
		
		age = day[2] - b_date[2] - ((day[0], day[1]) < (b_date[0], b_date[1]))
		
		mean += age
		count += 1

	return(int(mean/count))

#Similar to mySort, but instead of returning single
#Student, all of the sorted data is saved to a csv file.
def mySortPrint(a,col,fileName):
#Input: list of dictionaries, key to sort by and output file name
#Output: None

	#Your code here:
	sort = sorted(a, key = lambda x: x[col])
	keys = sort[0].keys()

	with open(fileName, 'w') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldnames = ["First", "Last", "Email"], extrasaction = "ignore")
		dict_writer.writerows(sort)
		

################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ",end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),40)
	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',15)
	total += test(mySort(data2,'First'),'Adam Rocha',15)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',15)
	total += test(mySort(data2,'Last'),'Elijah Adams',15)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',15)
	total += test(mySort(data2,'Email'),'Orli Humphrey',15)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],10)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],10)

	print("\nThe most common day of the year to be born is:")
	total += test(findDay(data),13,10)
	total += test(findDay(data2),26,10)
	
	print("\nThe average age is:")
	total += test(findAge(data),39,10)
	total += test(findAge(data2),41,10)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,10)


	print("Your final score is: ",total)
# Standard boilerplate to call the main() function that tests all your code.
if __name__ == '__main__':
    main()

