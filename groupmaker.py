# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 08:32:48 2022

@author: Isaac Young

# ***not done yet*** 1. extract out data from a pandas data frame generating 
#                             a. a list of all previous groups (var=prevpairs), 
#                             b. a list of all previous students (var=cumattendance),and 
#                             c. a list of all previous orphanpairings (var=orphansprevpairs)
#                             d. a list of all previous 3-person pairings (var=prevtriples) 
2. take attendance for the day while adding names for any new students to cumattendance. (var=attendance)
        no two students may have identical names
        no two styudents may have identical first and last names without a middle name or initial for both students.. 
            ---if one is added later.. ask for unique middle name or middle initials for both students
3. for each student in attendance, determine if there are any people who have no possible legal partners
        isolate those people as "orphans" (var=orphans) later those orphans will be paired off
4. using attendance determine a preliminary list of partners that are forced based on querying who is forced to have a single partner
        put that person with their only legal partner, (var=prelimforcedgroups)
5. resolve any conflicts that arrize from step 4 where one person is forced to choose between two or more people who both have the same single legal partner.
        randomly choose who gets to stay with a unique partner and who is forced to join the orphans (step 5 part a var=neworphans)
        report the truly legal forced groups (step5 part b var=forcedgroups)
        add those unlucky students to the orphans list (step5 part c var=orphans)
6. from a list of all attendees who are not orphans are are not in a forcedgroup, (var=remain_attendance) check if there are new forced pairings due to size constraints..
        6a. if the remaining attendance or orphans list is odd, move a randomly selected student to the orphans because everyone has to have a partner!
        6b. then, if the number of orphans is only 2 names long or the remaining attendance is only 2 names long, then those groups are forced too. 
7. run roundrobin pairing on remain_attendance
        7a. if the roundrobin pairing doesn't work, try other permutations in ordering (flipping first student in attendance order to last position)
        7b. if no simple permutation works in the roundrobin pairing.. move all the students in remain_attendance to the orphans list
        7c. if there are pairings generated. add those pairings to the prevpair list data
8. if there are any students in the orphans list.. run a new roundrobin pairing on these students to choose their partners (all of these should be repeat pairings)
        8a. if there are pairings generated, add these pairings to the orphansprevpairs list data

9. combine the groups created in steps 4, 5, 6, 7, and 8 together to generate the full group assignments for the week
10. from forcedgroups, move any new groups generated to the prevpair list data and move any repeated groups to the orphansprevpairings list

# ***not done yet*** 11. output a running data file in xlsx and another data file that contains this weeks attendance as well as the weeks's group assignments. 

# ***not done yet*** for students that have been assigned to join a 3-person group for the week:
#                         generate a running tally of the number of times each student has been put in a group of 3. randomly assign the bi week person to go with the group that 
#                         has the lowest overall score such that we can minimize the number of times each student gets put in a group of 3.

# ***not done yet*** store in pandas data frame
# week#; attendance; abscence list; group assignments this week
"""


import randomgroups as RG
import random

data=RG.filereader()
weeknum=RG.weeknumgetter(data)
cumattendance=RG.cumattendancegetter(data)
prevpairs=RG.prevpairsgetter(data)
"""
 need to write RG.getprevorphanpairs(data) fuctionality still
"""
#orphansprevpairs=RG.getprevorphanpairs(data)
orphansprevpairs=[]


weeknum=weeknum+1
print('this week:',weeknum)
returningstudents=RG.takeattendance(cumattendance)
attendance=RG.getnewnames(returningstudents ,cumattendance)
for n in attendance:
    if n not in cumattendance:
        cumattendance.append(n)
if len(attendance)%2==1:
    attendance.append('join another group')
    oddoneout=random.randrange(1,int(1+((len(attendance)-1)/2)))
    print()
    print()
    print('the odd person out must join group # ',oddoneout,'from the list')

"""
carry out step 3 now to see who are the orphans. (orhpans = students who have no possible partner this week and must go with someone a 2nd time)
and step 4 now to see who are the students who have only 1 possible partner
then step 5

"""
# prevpairs=[ ['a', 'b'], ['a', 'c'],  ['a', 'e'], ['a', 'f'], ['a', 'g'], ['a', 'h'], ['b', 'c'],  ['b', 'e'], ['b', 'f'], ['b', 'g'], ['b', 'h'], ['c', 'h'], ['c', 'e'], ['c', 'f'], ['c', 'g'], ['d', 'e'], ['d', 'f'], ['e', 'f']]
# attendance=['a', 'b', 'c', 'd', 'e', 'f', 'g','h']
unusedsummary=RG.arrayunusedpartners(attendance, prevpairs)
print('heres a summary of what students each student has as potential legal partners')
print('student: potential partners')
print(unusedsummary)
for n in unusedsummary:
    print(n,':',unusedsummary[n])
input('continue?')
orphans=RG.orphans(attendance, prevpairs) #step 3

print(f'the following people have already been partners with everyone else who attended class today at least once:{set(orphans)}')
prelimforcedgroups=RG.forcedpartners(attendance, prevpairs) #step 4

"""
note that so far, RG.conflictremover has worked well and promises to be more comprehensive.. but i haven't tested it atainst a lot of possibilities
RG.conflictresolver should do something similar but focuses more closely only on those conflicts where there are two students competing to be with a single student. 
"""

neworphans=RG.conflictremover(unusedsummary) #step 5 part a getting new orphans
forcedgroups=RG.forcedpartners_trimmer(neworphans, prelimforcedgroups) #step 5 part b getting a final list of forced groups
orphans+=neworphans #step5 part c getting final list of orphans

# orphans=['b', 'c', 'g']
# forcedgroups=[['a', 'd'], ['e', 'h']]
# attendance=['a', 'b', 'c', 'd', 'e', 'f', 'g','h']

remain_attendance=[x for x in attendance if x not in orphans]
partners1=[x[1] for x in forcedgroups]
partners2=[x[0] for x in forcedgroups]
allstu=partners1+partners2
for n in allstu:
    remain_attendance.remove(n) #begin step 6 logic


if  len(remain_attendance)%2==1: #step 6a
    unluckystudent=remain_attendance[random.randrange(len(remain_attendance))]
    orphans+=unluckystudent
    remain_attendance.remove(unluckystudent)
if len(orphans)==2: #step 6a
    forcedgroups.append(orphans)
    orphans=[]
if len(remain_attendance)==2: #step 6a
    forcedgroups+=[remain_attendance]
    remain_attendance=[]




countdown=len(remain_attendance)+1

if len(remain_attendance)>2:
    weeksgroups='bad group'
else:
    weeksgroups='skip'
    weeksgroups=[]
while weeksgroups=='bad group':
    countdown-=1
    remain_attendance=RG.attendanceswapper(remain_attendance)
    weeksgroups=RG.findweekspartners(remain_attendance,prevpairs,countdown)
if weeksgroups!='none':
    for n in weeksgroups:
        prevpairs.append(n)
    for n in forcedgroups:
        if set(n) not in [set(x) for x in prevpairs]:
            prevpairs.append(n)
        else:
            orphansprevpairs.append(n)
    
    
if weeksgroups=='none':
    input('something went wrong and the program couldnt find a solution. treating all students as orphans and recalculating')
    orphans+=remain_attendance
    remain_attendance=[]


print(str(remain_attendance)+'are the students remaining that have multiple options')
print(str(forcedgroups)+'these groups are forced in order to best follow the rules.')

countdown=len(orphans)
if len(orphans)>2:
    weeks_orphan_groups='bad group'
else:
    weeks_orphan_groups='skip'
    weeks_orphan_groups=[]
while weeks_orphan_groups=='bad group':
    countdown-=1
    setorphans=set(orphans)
    listsetorphans=list(setorphans)
    listsetorphans=RG.attendanceswapper(listsetorphans)
    weeks_orphan_groups=RG.findweekspartners(listsetorphans,orphansprevpairs,countdown)

allweeksgroups=weeksgroups+weeks_orphan_groups+forcedgroups

print('for week #',weeknum)
if 'join another group' in attendance:
    attendance.remove('join another group')
print('this weeks attendance was:',attendance)
print('this weeks groups will be:',allweeksgroups)
print('all pairs to date:',prevpairs)
print('cumulative list of all students to come to class:',cumattendance)
input('enter to exit')
filelineitem=[weeknum,attendance,allweeksgroups,prevpairs,cumattendance]
outfile=open('studentdata.txt', 'a')
outfile.write('\n'.join(list(map(str,filelineitem)))+'\n')
outfile.close()