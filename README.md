# Turing_Machine_Simulator
This is a simulator of a Turing Machine.
The program simulates a Turing Machine and analyzes input words, manipulates them, and determines a yes or no halt state. 
See the description.pdf to understand the format.

########################################################################
# Must-Knows & Pre-reqs
These are things you must know to understand the program:
1. Understand what a Turing Machine is and how it functions.
This video does a great job explaining it: https://www.youtube.com/watch?v=-ZS_zFg4w5k

########################################################################
# To Run the program:
1. Download the repository in a machine with Python installed.
2. Run the script from the command line using "python 'TM Simulator.py'"
3. Pass in the proper arguments as listed below

# Note
This program uses Pandas and Numpy (it was just practice for me), so it might be necessary that you install those packages in your environment.
Just run pip install pandas & pip install numpy and you should be good to go.

# Description Files
This repository contains 2 sample description files. Description01.txt and Description02.txt.
The alphabet for both files is '01'.

This is what they do:
Description01.txt - This configuration adds up the bits in the word, and gives the ultimate value 'ones place' value.
Description02.txt - This gives back the initial input with 1's flipped to 0 and 0's to 1's

########################################################################
# Arguments - 'TM Simulator.py' receives 4 command line arguments in the following order:
# A Definition File

This Definition File configures the Machine, following the format instructions specified in the Description file (Sescription.pdf).
# An Input file name

This file contains a series of words that the machine will analyze. This file follows the format instructions specified in the Description file (description.pdf).
# The output file name 

This file will be created as the output of the analysis of every line. It outputs according to the format instructions specified in the Description file (description.pdf).
# A limit of steps

To avoid inifite runs, this argument defines the limit of steps the machine can make when analyzing EVERY line of input. If the machine reaches the limit of steps when analyzing a word, it will HALT-LIMIT and return the current state. 
############################
############################

Any questions or comments just message me. Feel free to use my code for whatever the heck you want to.

