#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 21:17:46 2018

@author: Elizabeth Chan, Tessa Pham, Xinyi Wang

"""

"""
Structure:

1. Parsing the file

    - parseTXT() function parses the demo data file
        return students, preferences, classes, times, professorOfClass, classrooms, sizes
    - parseExcel() function to be added, to parse the excel data

This function incurs cheap costs.

2. Constructing the data

    - construct(students, preferences, classes)
        return studentsInClass, overlap, classes

    After we load the data in by either parseTXT() or parseExcel(), we feed the
    data into this construct function. The construct function takes inputs:
        students, preferences, classes, classrooms, sizesOfClassrooms, times
    and outputs:
        studentsInClass, overlap, classes, availableRoomsInTime

    The complexity of this function is O(k log k)+ O(w), which is the complexity to
    process the data

3. Assign the Classes to times
    assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,professorOfClass,times,overlap,classes)


"""

# parsing excel
import os
import pandas as pd
import xlrd
import copy
import csv
import datetime

# write multiple parse functions (for the demo file, for the preference lists of students, etc.) if necessary

# parsing for demo data
def parseTXT():
'''
Parses the constraints.txt and pref.txt, return roomSize, students, preferences, classes, times, professorOfClass.
Outputs look like:
    
students: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
classes: [6, 5, 4, 8, 1, 7, 3, 2]
preferences: [[], [7, 4, 2, 8], [2, 3, 4, 1], [4, 6, 5, 3], [3, 1, 7, 2], [5, 1, 3, 4], [7, 8, 2, 3], [5, 1, 2, 8], [2, 6, 8, 7], [2, 1, 3, 7], [3, 6, 4, 2]]
times: ['0', '1', '2', '3']
roomSize:{'1': 876, '2': 815, '3': 232, '4': 101}
professorOfClass: [0, '4', '4', '2', '1', '1', '3', '3', '2']

'''
    students = []
    preferences = []
    classes = []
    times = []
    professorOfClass = []
    roomSize = {}

    # preferences
    DSP1 = open("basic/pref.txt", "r") # opens file with name of "test.txt"
    preferencesInfo = DSP1.read().replace("\t", " ").replace("\n", " ").split(" ")
 
    for i in range(1, int(preferencesInfo[1]) + 1):
       students.append(str(i))

    temp = []
    count = 0
    for i in range (2, len(preferencesInfo)):
        if (count % 5 != 0):
            temp.append(preferencesInfo[i])
        count = count + 1

    count2 = 0
    individualPref = []
    preferences.append([])
    for i in range (0, len(temp)):
        individualPref.append(temp[i])
        count2 = count2 + 1
        if (count2 == 4):
            preferences.append(individualPref)
            count2 = 0
            individualPref = []

    DSP1.close()

    DC = open("basic/constraints.txt", "r")
    splitDemoCon = DC.read().replace("\t", " ").replace("\n", " ").split(" ")

    # classes
    for i in range(0, len(splitDemoCon)):
        if splitDemoCon[i] == "Classes":
            # for j in range(0, int(splitDemoCon[i + 1])):
            for j in range(1, int(splitDemoCon[i + 1]) + 1): # range(1, 15)
                classes.append(j) # classes[0..13] will store 1 - 14, same as students above!

    # parse classrooms and roomSize
    i = 0    
    while splitDemoCon[i] != "Rooms":
        i += 1
    totalNumOfRooms = int(splitDemoCon[i + 1]) + 1
    count = 0
    while count < totalNumOfRooms - 1:
        roomSize[splitDemoCon[i+2]] = int(splitDemoCon[i + 3])
        i += 2
        count += 1

    # times
    for i in range(0, int(splitDemoCon[2])):
        times.append(str(i))

    # professorOfClass
    professorOfClass = [0] # class 0 is not valid
    for i in range(0, len(splitDemoCon)):
        if splitDemoCon[i] == "Teachers":
            for j in range(i + 3, len(splitDemoCon), 2):
                professorOfClass.append(splitDemoCon[j])
    DC.close()
    ptemp = [[int(u) for u in x] for x in preferences]
    preferences = ptemp
    
    return roomSize, students, preferences, classes, times, professorOfClass


# parsing for bmc data:

def BMCparse():

    BMCexcel = pandas.read_excel('brynmawr/bmc-data-f17.xls')

    # times = [] has been replaced with following three lists 
    daysOfWeek = BMCexcel["Days 1"]
    startTime = BMCexcel["Srt1 AM/PM"]
    endTime = BMCexcel["End 1 AMPM"]

    classes = BMCexcel["Class Nbr"]

    professorOfClass = BMCexcel["Name"]

    # no list of students for students = []
    # instead use this array that is the number of student capacity 
    studentCap = BMCexcel["Class Cap"]


    print "\n\ndaysOfWeek \n {}".format(daysOfWeek)
    print "\n\nstartTime \n {}".format(startTime)
    print "\n\nendTime \n {}".format(endTime)
    print "\n\nclasses \n {}".format(classes)
    print "\n\nprofessorOfClass \n {}".format(professorOfClass)

    f = open("brynmawr_date.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in daysOfWeek:
        f.write("{}\n".format(i))
    f.close()


    f = open("brynmawr_startTime.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in startTime:
        f.write("{}\n".format(i))
    f.close()


    f = open("brynmawr_endTime.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in endTime:
        f.write("{}\n".format(i))
    f.close()

    allTime = zip(daysOfWeek, startTime, endTime)
    f = open("brynmawr_allTimes.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in allTime:
        f.write("{}\n".format(i))
    f.close()
    return daysOfWeek, startTime, endTime, classes, professorOfClass


    # data not availble from excel file
    # preferences = [] 

def HCparse():
    # HCexcel = pandas.read_excel('haverford/haverfordEnrollmentDataS14.csv')

    with open('haverford/haverfordEnrollmentDataS14.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        dates = []
        colors = []
        for row in readCSV:
            # times = [] has been replaced with following three lists 
            daysOfWeek = row[18]
            startTime = row[13]
            endTime = row[16]

            classes = row[1]

            professorOfClass = row[11]
            # colors.append(color)

        print(daysOfWeek[0])
        # print(colors[0])

    # print daysOfWeek
    # print startTime
    # print endTime
    # print classes
    # print professorOfClass


    # data not availble from excel file
    # students = []
    # preferences = [] 

# Convert times to 24-hour format (for comparison).

def convertTimes(startTime, endTime):
    for i in range(0, len(startTime)):
        st = startTime[i]
        et = endTime[i]
        startTime[i] = datetime.datetime.strptime(st, '%I:%M %p').time()
        endTime[i] = datetime.datetime.strptime(et, '%I:%M %p').time()
    # startTime and endTime now contain time objects that can be compared to one another.
    return startTime, endTime
    


# parameter: a 3-tuple (daysOfWeek, startTime, endTime). Account for overlapping times.
def refineTimeList(timeTuples):
    # remove duplicate times
    timeTuples = set(timeTuples)

    MWF = [t for t in timeTuples if t[0] in ['M', 'W', 'F', 'MW', 'WF', 'MF', 'MWF']]
    TTH = [t for t in timeTuples if t[0] in ['T', 'TH', 'TTH']]

    i = 0
    for j in range(1, len(MWF)):
        # if start time of this slot is earlier than the finish time of the original slot
        if MWF[j][1] < MWF[i][2]:
            MWFList[i].append(MWF[j])
        else:
            i += 1
            MWFList[i].append(MWF[j])
    
    i = 0
    for j in range(1, len(TTH)):
        if TTH[j][1] < TTH[i][2]:
            TTHList[i].append(TTH[j])
        else:
            i += 1
            TTHList[i].append(TTH[j])
    
    return MWFList, TTHList

# Next level for constructing the inputs.
def construct(students, preferences, classes, roomSize, times):
# def construct(students, preferences, classes, classrooms, sizesOfClassrooms, times):

    # ASSUME that classes is a list of tuples: c in classes = (major, class #)

    # studentsInClass: a dictionary (key = class, value = list of students in that class)
    studentsInClass = {c: [] for c in range(0, 15)}
    studentsInClass.get(0).append(0)
    # overlap: a 2D matrix (row = all classes, column = all classes, entry at (i, j) = # of students taking both classes i and j)
    overlap = [[0 for c in range(0, 15)] for c in range(0, 15)]
    # overlap = [[0 for c in classes] for c in classes]
    majors = [c[0] for c in classes]
    relation = [[0 for m in majors] for m in majors]

    for s, p in zip(students, preferences):
        # for each class c in the preference list of student s
        for c in p:
            # add s to student list of class c
            if studentsInClass[c]==None:
                studentsInClass[c]=[s]
            else:
                studentsInClass[c].append(s)
            # increment the overlaps of class c with each class in the rest of list p
            for other_c in p[(p.index(c) + 1):]:
                # in overlap and any other arrays we construct, all classes are 1 less than their original numbers in the data
                overlap[c][other_c] += 1
                overlap[other_c][c] += 1

                # construct relation between 2 majors
                relation[c[0]][other_c[0]] += 1
                relation[other_c[0]][c[0]] += 1
    # the idea is: we want to sort the array classes, but we have to get the size from len(studentsInClass.get(c)) for each c in classes
    sizes = [len(studentsInClass.get(c)) for c in classes]
    # sortedClasses = [x for _, x in sorted(zip(sizes, classes))]
    classes = sortedClasses

# sort the classroom from small to big, paired with their size.
#    sortedClassroom=[(y, x) for x, y in sorted(zip(sizesOfClassrooms, classrooms))]
    
    sortedClassroom = [(k, roomSize[k]) for k in sorted(roomSize, key = roomSize.get, reverse = False)]
    
    # availableRoomsInTime: a dictionary (key = time, value = list of tuples (room, size), ranked from smallest to largest)
    availableRoomsInTime = {t: sortedClassroom for t in times}
    return studentsInClass, overlap, classes, availableRoomsInTime


def assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,professorOfClass,times,overlap,classes,timeOfClass,roomOfClass):
    # sort the classroom from small to big, paired with their size.
    sortedClassroom = [(y, x) for x, y in sorted(zip(sizesOfClassrooms, classrooms))]
    # availableRoomsInTime: a dictionary (key = time, value = list of tuples (room, size), ranked from smallest to largest)
    availableRoomsInTime = {t: sortedClassroom for t in times}

    # CONSTRUCT RELATION BETWEEN EVERY 2 MAJORS


    return studentsInClass, overlap, classes, availableRoomsInTime


def assignClassToTime(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, professorOfClass, times, overlap, classes, timeOfClass, roomOfClass):
    min_overlap = float("inf")
    chosen_time = times[0]

    prof = professorOfClass[c]

    for t in times:
        # skip if the professor teaching class c is already teaching another class in this time
        if (len(professorsInTime[t]) != 0) & (prof in professorsInTime[t]):
            continue

        # skip if no more available rooms
        if len(availableRoomsInTime[t]) == 0:
            continue

        # skip if number of students in class c is greater than the size of the biggest available room in time t
        if len(studentsInClass.get(c)) > availableRoomsInTime[t][-1][1]:
            continue

        count = 0
        for assigned_c in classesInTime[t]:
            count += overlap[c][assigned_c]
# now you need to do, for assigned_c in classesInTime[t] and classesInTime[ALL SLOTS OVERLAPING WITH T]
#{TIME_SLOTS: ALL TIME SLOTS OVERLAPPING WITH THIS TIME SLOTS}
#
#   def process_time_inputs(day, start_time, end_time):
#       for i in range(0,len(day))
#
        if count < min_overlap:
            min_overlap = count
            chosen_time = t

    # add class c to the chosen time
    classesInTime[chosen_time].append(c)
    # add the professor teaching class c to the list of professors occupied in the chosen time
    professorsInTime[chosen_time].append(prof)
    temp = copy.deepcopy(availableRoomsInTime[chosen_time])
    roomOfClass[c] = temp.pop()[0]
    availableRoomsInTime[chosen_time] = copy.deepcopy(temp)
    timeOfClass[c] = chosen_time


# This function is for optimality analysis.
def calculateStudentsInClass(timeOfClass, classes, students, preferencesDict):
    studentsTakingClass = {}
    for c in classes:
        studentsTakingClass[c] = []
    for s in students:
        busyTime = []
        wishList = preferencesDict[s]
        for i in range(0,4):
            if timeOfClass[wishList[i]] not in busyTime:
                busyTime.append(timeOfClass[wishList[i]])
                studentsTakingClass[wishList[i]].append(s)
            # else, just pass
    return studentsTakingClass
# need to change to a more complicated algorithm to maximize the overal optimality
# brute force: which class to prioritize to receive the largest # classes out of 4.



def main():
    roomSize, students, preferences, classes, times, professorOfClass = parseTXT()
    studentsInClass, overlap, classes, availableRoomsInTime = construct(students, preferences, classes, roomSize, times)

#Now, initialize two arrays to store the results.
    # classesInTime: a dictionary (key = time, value = list of classes in that time)
    classesInTime = {t: [] for t in times}
    # professorsInTime: a dictionary (key = time, value = list of professors teaching a class in that time)
    professorsInTime = {t: [] for t in times}

    professorOfClass = {}
    for c in classes:
        professorOfClass[c]=professorOfClass[int(c)]
        
# below are some reorganization for the outputs
    roomOfClass = {} #courseID: roomID
    timeOfClass = {} #courseID: timeID
    for c in classes:
        assignClassToTime(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, professorOfClass, times, overlap, classes, timeOfClass, roomOfClass)

    preferencesDict = {}
    for s in students:
        preferencesDict[s] = preferences[int(s)]

# Now calculate optimality.

    studentsTakingClass = calculateStudentsInClass(timeOfClass, classes, students, preferencesDict)

    f = open("schedule.txt", "w+")
    f.write("Course" + '\t' + "Room" + '\t' + "Teacher" + '\t' + "Time" + '\t' + "Students" + '\n')
    for i in range(len(classes)):
        c = classes[i]
        f.write(str(c)+'\t'+str(roomOfClass[c])+'\t'+professorOfClass[c]+'\t'+timeOfClass[c]+'\t'+' '.join(studentsTakingClass[c])+'\n')   
    with open("schedule.txt") as f:
        print(f.read())
    
    total = 0
    for key in studentsTakingClass:
        total += len(studentsTakingClass[key])
    opt = total / (len(students) * 4)
    print(opt)

"""
    print('\n')
    print('\n')
    print("Below are what's returned by parseTXT: "+'\n')
    print("students,", students)
    print("classes,", classes)
    print("preferences", preferences)
    print("times",times)
    print("roomSize",roomSize)
    print("professorOfClass",professorOfClass)
    
    print('\n'+"OtherThings"+'\n')
    
    print("roomOfClass",roomOfClass)
    print("professorOfClass",professorOfClass) #{7: '7', 10: '3'}
    print("timeOfClass",timeOfClass)
    print("studentsTakingClass",studentsTakingClass)
    print(students, '\n','\n', preferences,'\n','\n',classes,'\n','\n',times,'\n','\n',professorOfClass)

"""
if __name__ == "__main__":
    main()
