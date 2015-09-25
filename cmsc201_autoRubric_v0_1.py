##################################################################################
# Script : cmsc201_autoRubric_v0_2.py [CMSC201 Rubric Autocomplete (v0.2)]
# Author : Akshay Peshave (peshave1@umbc.edu)
# Desc	 : This scripts autocompletes the rubric for a given
#	   student including computation of total points. 
#	   The graders/TAs need only fill out those entries of the 
#	   rubric for which they are deducting points (and include
#	   any comments/suggestions they wish at the end of the 
#	   rubric). Once done they can execute this script from 
#	   within the homework folder (e.g. HW1, HW2, Lab1 etc.)
#	   for that particular student as follows:
#		python [script_name] [student_id]
#	   E.g. python cmsc201_autoRubric_v0_1.py peshave1
# 
# Revisions in v0.2:
#	1. Improved regex matching for rubric rows to support fractional values
#	   for grades.
#	2. Minor code refactoring.
# Upcoming revisions:
#	1. execute script once in homework/lab folder to 
#	   autocomplete rubrics in all student folders available 
#	   in the hw/lab folder.
##################################################################################

import io
import sys
import re
from shutil import move
from os import remove

totalPoints = 0.0
student="./"+sys.argv[1]

with open(student + "/rubric_new.txt", "wb") as newRubricFile:
    with open(student + "/rubric.txt", "rb") as rubricFile:
        for line in rubricFile:
            if str(line).startswith("@"): # replace '@' with full points for that entry in the rubric
                entryLength = len(line.split(" ")[0].split("/")[0])
                line = line.split(" ")[0].split("/")[1] + line[entryLength:]

            # update total points if rubric line is pre-filled or is the "Total Points" line 
            lineBeginning = line.split(" ")[0]
            if re.match(r"[0-9]+(.[0-9]+)?/[0-9]+(.[0-9]+)?", lineBeginning):
                totalPoints = totalPoints + float(lineBeginning.split("/")[0])
            elif lineBeginning == "Total":
                totalLineTokens = line.split(":")
                line = totalLineTokens[0] + ": " + str(totalPoints) + "/" + totalLineTokens[1].strip().split("/")[1]+"\n"
            
            newRubricFile.write(line)

#backup original rubric and replace with auto-filled rubric
move(student + "/rubric.txt", student + "/rubric_backup.txt")
move(student + "/rubric_new.txt", student + "/rubric.txt")
            

