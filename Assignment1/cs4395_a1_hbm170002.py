import sys
import csv
import re
import pickle

#Person class that contains all the person's data as well as a display function
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee id:",self.id)
        print("\t",self.first,self.mi,self.last,sep=" ")
        print("\t",self.phone)

#function to process the input and modify it so that its in the correct format
def processInput(filename):

    resultDict = {}
    #opening the file and reading it line by line
    with open(filename, mode='r') as csv_file:
        #splitting the line into a list of strings separated by commas
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        #reading each line and modifying it
        for row in csv_reader:
            if line_count != 0: #ignoring the first line
                #changing the first and last names to Capital Case
                row[0] = row[0].capitalize()
                row[1] = row[1].capitalize()
                #checking to see if middle initial is provided in correct format and changing it to uppercase
                if (len(row[2])==1):
                    row[2] = row[2].upper()
                else:
                    #if middle is incorrect format or empty, then using 'X' as middle initial
                    row[2] = 'X'

                #using regex to make sure that id is in the correct format and asking user to re-enter id if it is not in the correct format
                regexIDResult = re.search("^[a-zA-Z]{2}\d{4}$", row[3])
                newID = row[3]

                #looping until user inputs id in the correct format
                while not regexIDResult:
                    print("ID invalid: ", newID)
                    print("ID is two letters followed by 4 digits")
                    newID = input("Please enter a valid id: ")
                    regexIDResult = re.search("^[a-zA-Z]{2}\d{4}$", newID)
                row[3] = newID

                #using regex to make sure that phone number is in the correct format and asking user to re-enter the number if its not correct
                regexNumResult = re.search("^\d{3}-\d{3}-\d{4}$",row[4])
                newNum = row[4]

                #looping until user inputs phone number in the correct format
                while not regexNumResult:
                    print("Phone ", newNum, "is invalid")
                    print("Enter phone number in form 123-456-7890")
                    newNum = input("Enter phone number: ")
                    regexNumResult = re.search("^\d{3}-\d{3}-\d{4}$",newNum)
                row[4] = newNum

                #now that all the data is correct, creating a person object with this data
                p1 = Person(row[0],row[1],row[2],row[3],row[4])

                #checking to see if there is a duplicate id
                if row[3] in resultDict:
                    print("ERROR: ID is repeated in input file")
                    exit(1)

                #adding the new person object into the dictionary with id as the key
                resultDict.update({row[3]:p1})

            line_count += 1

    return resultDict

def main():

    #checking to see if the user provided the relative data path in sysarg
    if len(sys.argv) < 2:
        print("ERROR: Data path was not provided")
        exit(1)

    #extracting filename from sysarg
    filename = sys.argv[1]

    #calling the processInput function to modify the input into the correct format
    resultDict = processInput(filename)

    #saving resulting dictionary in pickle file
    pickle.dump(resultDict, open('dict.p', 'wb'))

    #reading the dictionary from pickle file
    dict_in = pickle.load(open('dict.p', 'rb'))  # read binary

    print("Employee List:\n")
    for id in dict_in:
        print("\n")
        dict_in[id].display()


if __name__ == "__main__":
    main()



