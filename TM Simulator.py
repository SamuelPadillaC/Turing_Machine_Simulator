########################################
# Created by Samuelito Perro #
########################################
# This is a NON-DETERMINISTIC Finite State Automata Simulator
# This program takes 3 parameters: An NFSA detinition file,
# A file holding strings, An output file name.
# check description document for the format of these files

from datetime import datetime
import time, sys
import numpy as np
import pandas as pd

start = time.time()
print ("Art by Samuel Padilla, a.k.a. Samuelito Perro")
#################################
#           CLASSES             #
#################################

class Turing_Machine:
    #Initialize values for the Machine
    def __init__(self, Path):
        self.vector_lines = []
        
        #Calling functions
        self.ReadTM(Path)
        if (self.Create_Table()): #On succesful creation, print dataframe
            print("\n\n====================================================",
            "\nSUCCESFUL CONFIGURATION OF SPECIFIED TM.",
            "\nIt has the following transition table:\n\n",
            self.Transition_Table,
            "\n====================================================")

    def ReadTM (self, Path):
        # Opening the file #
        file_object = open(Path, 'r')
        self.vector_lines = (file_object.readlines()) # Reads all the lines into the vector vector_lines
        file_object.close()
        
        # Define Alphabets
        self.Input_alphabet =  self.vector_lines[0][:-1]    
        self.Tape_alphabet = self.vector_lines[1][:-1]

        #Checking Input Alphabet
        for i in self.Input_alphabet:
            if ord(i) < 33 or ord(i) > 126:
                print ("\nINPUT ALPHABET ERROR: The are invalid characters in the Input Alphabet.",
                    "\nThe valid characters have ASCII codes in the range 33 - 126",
                    "\nThe character to raise the exception was '%s'" % i)
                exit()

            if i not in self.Tape_alphabet: #All elements of Input must be in Tape
                print ("\nINPUT ALPHABET ERROR: The are characters in the Input Alphabet",
                    "that are not part of the Tape Alphabet",
                    "\nThe character to raise the exception was '%s'" % i)
                exit()

        #Chekcing Tape Alphabet
        if self.Tape_alphabet[0] != ' ': #First char must be ' '
            print("\nTAPE ALPHABET ERROR: The tape alphabet does not contain the frist character as a ' ' (space).")
            exit()
        
        for i in self.Tape_alphabet:
            if ord(i) < 32 or ord(i) > 126:
                print ("\nTAPE ALPHABET ERROR: The are invalid characters in the TAPE Alphabet.",
                    "\nThe valid characters have ASCII codes in the range 32 - 126",
                    "\nThe character to raise the exception was '%s'" % i)
                exit()

        #Getting Number of states
        try:
            self.States = int(self.vector_lines[2][:-1]) 
        except ValueError:
            print("\nERROR: The value of the third line is not a valid integer.",
            "\nYou entered:", self.vector_lines[2][:-1])
            exit()

        # Check if the number of lines matches the number of states #
        if self.States != len(self.vector_lines[3:]):
            print("\nERROR: The last n lines of the TM description file do not match the number of tates.",
            "\nThere should be", self.States, "final lines and there is", len(self.vector_lines[3:]), "lines.")
            exit()

    def Create_Table (self):
        # Creating raw_table -> this will be used to create the dataframe #
        raw_table = []

        # Manipulating the last n rows
        for row in self.vector_lines[3:]:
            row = row.strip('\n') #Striping last '\n' character of every line
            row = row[1:-1].split('][') #Split the row (discarding first and last characters) by ']['
            #Check size of row
            if (len(row) != len(self.Tape_alphabet)):
                print("\nTABLE ERROR: The number of triplets in each row must match the number of characters in the Tape Alphabet",
                    "\nThe row that raised the exception was:", row)
                exit()

            raw_table.append(row) #Append row to raw_table
        
        # Creating Pandas Dataframe #
        self.Transition_Table = pd.DataFrame(raw_table, columns=list(self.Tape_alphabet))

        if (self.Verify_Table()):
            return 1

    def Verify_Table (self):
        #Loop through each column as a pandas series
        for column in self.Transition_Table:
            #Checking every triplet in each series using int iteration
            for row in range(0, self.Transition_Table[column].size):
                #Check first argument
                if self.Transition_Table[column][row][0] not in ['R', 'L']:
                    print("\nTABLE ERROR: The triplet in column '%s'"
                        % column,
                        "index", row,
                        "contains an invalid first argument.",
                        "\nThe valid characters are only 'R' or 'L'",
                        "\nThe triplet was: ", self.Transition_Table[column][row])
                    exit()

                #Check second argument
                if self.Transition_Table[column][row][2] not in self.Tape_alphabet:
                    print("\nTABLE ERROR: The triplet in column '%s'"
                        % column,
                        "index", row,
                        "contains an invalid second argument.",
                        "\nThe valid characters are: '%s'" % self.Tape_alphabet,
                        "\nThe triplet was: ", self.Transition_Table[column][row])
                    exit()

                #Check third argument - accoutn for negative numbers by grabbing from 3 char on.
                try: #Check for not int
                    n = int(self.Transition_Table[column][row][4:])
                except ValueError:
                    print("\nTABLE ERROR: The triplet in column '%s'"
                        % column,
                        "index", row,
                        "contains an invalid third argument.",
                        "\nThe character must be a number",
                        "\nThe triplet was: ", self.Transition_Table[column][row])
                    exit()

                if ((n < 0 or n >= self.States) and n != -1 and n != -2): #Check range
                    print("\nTABLE ERROR: The triplet in column '%s'"
                        % column,
                        "index", row,
                        "contains a third argument out of range.",
                        "\nThe character must be in the range 0 -", self.States-1,
                        "or it must be -1 or -2."
                        "\nThe triplet was: ", self.Transition_Table[column][row])
                    exit()

        return 1                        
    

##########################################
#            DRIVER FUNCTION             #
##########################################

def main():
    # Checking for the amount of parameters #
    if len(sys.argv) != 5:
        print("\n USAGE: Please enter 3 parameters in the following order:")
        print("1. A TM definition file\n2. An Input file name. It should hold strings, one per line. \n3. An Output file name \n4. The maximum number of steps the machine is allowed to perform.")
        exit()

    # Checking fourth parameter #
    try:
        limit = int(sys.argv[4])
    except ValueError:
        print("\nPARAMETER ERROR: The last parameter must be a positive number",
            "\nThe parameter entered was: ", limit)
        exit()
    #Check value
    if limit < 0:
        print("\nPARAMETER ERROR: The last parameter must be a positive number",
            "\nThe parameter entered was: ", limit)
        exit()

    # Reading file and creating machine #
    TM = Turing_Machine(sys.argv[1])

    # Read and Verify Input File #
    Input_lines = Read_Input(sys.argv[2], TM.Input_alphabet)

    # Run the Machine #
    Run_Machine (Input_lines, TM.Transition_Table, sys.argv[3], limit)

    #################################################
    # Final Message #
    print("\n\nSuccesful run. Check", sys.argv[3], "file.")
    print ("\nExecution time was: ", time.time() - start)


#################################
#           FUNCTIONS           #
#################################

def Read_Input (Path, Alphabet):
    # Open and Read File #
    file_object = open(Path, 'r')
    Input_lines = (file_object.readlines()) # Reads all the lines into Input_lines
    file_object.close()

    # Check that all Lines are valid #
    Return_list = []
    for line in Input_lines: #Loop through each line
        line = line.rstrip('\n') #Strip the last '\n' from each line

        if line != '': #Only check non empty lines
            for char in line: #Check each character
                                
                #If invalid char, print error but still append.
                if char not in Alphabet:
                    print ("\nERROR READING INPUT FILE: The word '%s' contains an invalid character." % line)
                    exit()
            
            #Append line to return list if all chars are valid
            Return_list.append(line)
        
        else: #Empty lines are valid, they are empty strings
            Return_list.append('') 

    #Corner Case - If the last character of the last item of the Input File is a '\n'
    if (Input_lines[-1][-1] == '\n'): 
        Return_list.append('') #This means the last line is an empty line. Still append

    # Print Succesful read of Input Lines #
    print("====================================================",
        "\nSUCCESFUL READ OF INPUT FILE -", Path,
        "\nThe strings to be processed are:\n")
    print(Return_list,
        "\n====================================================")

    return Return_list

#################################################
#################################################

def Run_Machine (Input, Table, Output_File, limit):
    #Opening the output file and write date log #
    Output = open(Output_File, 'w')
    Output.write("Running TM Simulator by Samuel Padilla\n")
    Output.write("Run Time: %s\n\n" % datetime.now().strftime("%d/%m/%Y %H:%M"))

    #Looping through each input
    for word in Input:
        #Put word in the tape starting on square 1
        Tape = [' ']
        if word == '': Tape.append(' ')    
        for i in list(word): Tape.append(i)
        
        # Head starts pointing to 1, state starts at 0, step starts at 1 #
        head = 1
        step = 1
        state = 0

        # Writing to output before execution
        Output.write("====================\n")
        Output.write("'%s'\n" % word)

        #Loop of execution
        while (1):
            if step > limit:
                Output.write("State %s. | HALT-LIMIT\n" % state)
                break

            ### Finding triplet Match ###
            try:
                current_char = Tape[head] #Read char in header
            except IndexError:
                Tape.append(' ') #Append an extra blank to the tape
                current_char = Tape[head] #Read char again from header
                
            triplet = Table[current_char][state] #Look for [char][state] coordinate


            ### Reading triplet ###
            #Write to tape
            Tape[head] = triplet[2]

            #Update head
            if triplet[0] == 'R':
                head += 1
            else:
                head -= 1

            #Check head for badmove
            if head < 0:
                Output.write("State -3. | HALT-BADMOVE\n")
                break

            #Update state
            state = int(triplet[4:])


            ### Check for good halts ###
            if state == -1: #TM says NO 
                Output.write("State -1. | HALT-NO\n")
                break
            elif state == -2: #TM says YES
                Output.write("State -2. | HALT-YES\n")
                break

            # Add to step 
            step += 1

        Output.write("%s\n" % Tape)

#################################################
#################################################
# Calling the main function first #
if __name__ == "__main__":
    main ()
#####################