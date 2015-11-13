##################################################################################
# Script : cmsc201_autoRubric_v0_2.py [CMSC201 Rubric Autocomplete (v0.3)]
# Author : Akshay Peshave (peshave1@umbc.edu)
# Desc	 : This scripts autocompletes the rubric for all 
# 	   students in a give HW folder including computation of total points. 
# 	   The graders/TAs need only fill out those entries of the  individual
# 	   rubrics for which they are deducting points (and include
# 	   any comments/suggestions they wish at the end of the 
# 	   rubric). Once done they can execute this script from 
# 	   within the homework folder (e.g. HW1, HW2, Lab1 etc.) for their
# 	   own TA folder as follows:
# 		    python [script_name] [TA_id]
# 	   E.g. python cmsc201_autoRubric_v0_1.py peshave1
# 
# Revisions in v0.3.0:
#    1. Implemented iterative rubric completion for all students in a HW folder
#        in one exectution of the script.
#    2. Fixed bug which caused incorrect line updates when line contains tab.
#        (FIX: change line.split(" ") to line.split())
##################################################################################

import io
import os
import sys
import re
from shutil import move
from os import remove


homeworkFolder = "./" + sys.argv[1] + "/"
studentFolders = os.listdir(homeworkFolder)

# update rubric files for all students in the given homework folder
for studentFolder in sorted(studentFolders):
    studentFolderPath = homeworkFolder + studentFolder
    totalPoints = 0.0
    with open(studentFolderPath + "/rubric_new.txt", "wb") as newRubricFile:
        with open(studentFolderPath + "/rubric.txt", "rb") as rubricFile:
            for line in rubricFile:
                lineTokens = line.split()
                updatedLine = line
                
                if (len(lineTokens) <> 0):
                    # update logic for individual rubric line
                    if str(updatedLine).startswith("&"):  # replace '&' with full points for that entry in the rubric
                        entryLength = len(lineTokens[0].split("/")[0])
                        updatedLine = lineTokens[0].split("/")[1] + updatedLine[entryLength:]
        
                    # update logic if rubric line is pre-filled or is the "Total Points" line 
                    lineBeginning = lineTokens[0]
                    if re.match(r"[0-9]+(.[0-9]+)?/[0-9]+(.[0-9]+)?", lineBeginning):
                        totalPoints = totalPoints + float(lineBeginning.split("/")[0])
                    elif lineBeginning.lower() == "total":
                        totalLineTokens = updatedLine.split(":")
                        updatedLine = totalLineTokens[0] + ": " + str(totalPoints) + "/" + totalLineTokens[1].strip().split("/")[1] + "\n"
    
                newRubricFile.write(updatedLine)
    
    # backup original rubric and replace with auto-filled rubric
    move(studentFolderPath + "/rubric.txt", studentFolderPath + "/rubric_backup.txt")
    move(studentFolderPath + "/rubric_new.txt", studentFolderPath + "/rubric.txt")
    print("Processed student " + studentFolder)
