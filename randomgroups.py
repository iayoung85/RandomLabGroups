"""
Weekly Random Group generator
By Isaac Young
03-26-2017

program written to satisfy the need to assign random groups each week that do not repeat throughout the semester. 

step 1: using a list of all different students that have attended lab to date, take attendance then add new students who have not attended lab in previous weeks. Add the new students to the list of all students who have ever attended the lab
step 2: if the attendance list is an odd number of students. add a fake student to the list for picking random groups then have the person with the fake student join another random group.
step 3: using the current week's attendance (with or without the fake student), use the round robin tournament algorithm to generate a set of all possible different weeks where # of different weeks is n minus 1.
step 4: pick a random week from step 2 such that no 2-person group used in previous weeks is repeated
step 5: return the following: 
    1. this week's group assignments: a random week from the set of all weeks such that it does not repeat any pairing from any previous week. 
    2. an updated set of all group assignments used thus far since the beginning of the semester
    3. This week's attendance list.
    4. an updated list of all students that have ever attended the lab.
    5 week number

"""
#function that opens a file called studentdata.txt 
def filereader():
    errco=0
    while errco==0:
        try:
            with open('studentdata.txt','r') as infile:
                allprevdata=list(infile)
            infile.closed
            errco=1
        except:
            outfile=open('studentdata.txt','w')
            outfile.close
            continue
        
        return allprevdata
def weeknumgetter(allprevdata):
    if allprevdata==[]:
        weeknum=0
    else:
        selecteddata=[]
        for n in range(-5,0,1):
            selecteddata.append(allprevdata[n])
        weeknum=int(selecteddata[0])
    return weeknum

def cumattendancegetter(allprevdata):
    if allprevdata==[]:
        cumattendance=[]
    else:
        selecteddata=[]
        for n in range(-5,0,1):
            selecteddata.append(allprevdata[n])
        import ast
        cumattendance=ast.literal_eval(selecteddata[-1])
    return cumattendance
    
def prevpairsgetter(allprevdata):
    if allprevdata==[]:
        prevpairs=[]
    else:
        selecteddata=[]
        for n in range(-5,0,1):
            selecteddata.append(allprevdata[n])
        import ast
        prevpairs=ast.literal_eval(selecteddata[-2])
    return prevpairs


#function that will compare a list of groups to find an identical copy to [['a', 'b'], ['c', 'd'], ['join another group', 'e'], ['f', 'g']]

def group_copy_finder(inputgrouplist,referencelist):
    # referencelist=[['a', 'b'], ['c', 'd'], ['join another group', 'e'], ['f', 'g']]
    if referencelist==[]:
        input('this ref list is empty, press enter to continue')
        return "this aint identical"
    for n in inputgrouplist:
        if n not in referencelist and [n[1],n[0]] not in referencelist:
            return "this aint identical"
    # input('woohoo we found the copy! press enter to continue')
    return "this is identical"
# group_copy_finder([['c', 'g'], ['d', 'h'], ['b', 'e'], ['a', 'f']],[['d', 'h'], ['g','c'], ['b', 'e'], ['a', 'f']])


#given list of unique names with an even numbered list, returns a matrix of pairings for n-1 weeks where n is length of list
def roundrobinmaker(fulllist):
    if len(fulllist)%2==1:
        input('there was a critical error in the round robin algorithm enter to continue')
        return 'error roundrobin'
    matrix=list()
    splitset=listsplitter(fulllist)
    mergedset=splitsetmerger(splitset)
    matrix.append(mergedset)
    for n in range(int(len(fulllist)-2)):
        splitset=rotater(splitset)
        mergedset=[]
        mergedset=splitsetmerger(splitset)
        matrix.append(mergedset)
    # import random
    # for n in matrix:
    #     print(n)
    #     # input('press enter to continue')
    #     group_copy_finder(n)
        # random.shuffle(n)
    return(matrix)

#split fulllist into 2: set1 and set2
def listsplitter(fulllist):
    set1=[]
    set2=[]
    for n in range(int(len(fulllist)/2)):
        set1.append(fulllist[n])
        set2.append(fulllist[-n-1])
    set2.reverse()
    returnset=[set1,set2]
    return returnset

# fix the 0th item in set1 and rotate all others clockwise by 1
def rotater(splitset):
    toprowendperson=splitset[0][-1]
    bottomrowfrontperson=splitset[1][0]
    splitset[0].remove(toprowendperson)
    splitset[0].insert(1,bottomrowfrontperson)
    splitset[1].remove(bottomrowfrontperson)
    splitset[1].append(toprowendperson)
    return(splitset)

#takes a split set of two lists of equal length and pairs the nth value from each set returns a list of pairs
def splitsetmerger(splitset):
    mergedgroups=[]
    for n in range(int(len(splitset[0]))):
        mergedgroups.append([splitset[0][n],splitset[1][n]])
    return mergedgroups

#checks to see if a group is in a matrix of lists of groups, returns a new matrix containing only the rows of the original matrix where the group was not contained
def checkforgroup(matrix,group):
    listn=[]
    for n in matrix:
        if group not in n and [group[1],group[0]] not in n:
            listn.append(n)
    return listn

#given a *matrix* of list of groups, returns a *new_matrix* containing only the rows of the original *matrix* where all of the groups in the list *all_groups* are not used
def checkforallgroups(matrix,all_groups):
    new_matrix=list()
    for n in matrix:
        new_matrix.append(n)
    for n in all_groups:
        new_matrix=checkforgroup(new_matrix,n)
    if len(new_matrix)==0:
        #print('there are not possible combinations where no one will have a repeat partner')
        return 'none'
    else:
        return new_matrix

#takes an attendance list, puts the first name in the list in last position.
def attendanceswapper(attendance):
    lastitem=attendance[len(attendance)-1]
    retlist=list()
    retlist.append(lastitem)
    for n in range(len(attendance)-1):
        retlist.append(attendance[n])
    return retlist

#this function takes a list, and outputs a new list of all possible permutations in order of the inputed list only retreives 50 different permuations for the sake of speed.
def quickperm(inlist,memlimit):
    count_limiter=1
    N = len(inlist)
    p = list(range(0, N+1))
    i = 1
    outlist=[]
    outlist.append(str(inlist))
    while i < N:
        p[i] -= 1
        if i % 2 == 1:
            j = p[i]
        else:
            j = 0
        inlist[j], inlist[i] = inlist[i], inlist[j]
        outlist.append(str(inlist))
        count_limiter+=1
        if count_limiter==memlimit:
            break
        i = 1
        while p[i] == 0:
            p[i] = i
            i += 1
    import ast
    newint=0
    for n in outlist:
        outlist[newint]=ast.literal_eval(n)
        newint+=1
    return(outlist)


#given an *attendance* list, prints a combination of groups (*todayspartners*) where no one has a repeat partner then edits the list of previous groups (*prvgroups*) to include chosen set of groups
def findweekspartners(attendance,prvgroups,countdown):
    if countdown==-1:
        return 'none'
    matrixallposspairs=roundrobinmaker(attendance)
    legalweeks=checkforallgroups(matrixallposspairs,prvgroups)
    if legalweeks=='none':
        return 'bad group'
    import random
    todayspartners=legalweeks[random.randrange(len(legalweeks))]

    return todayspartners

#from the total list of all students to come to class, populates a list of those students who attended this week.
def takeattendance(masterstudentlist):
    attendancelist=list()
    student=''
    everyonehere=input('is everyone here? y/n').upper()
    if everyonehere=='Y':
        for n in masterstudentlist:
            attendancelist.append(n)
        return attendancelist
    for n in masterstudentlist:
        print(n)
        student=input("is he or she present? y/n").upper()
        print()
        if student=='Y':
            attendancelist.append(n)
    return attendancelist


"""
given a name and two lists of names, looks to see if first name and last name in the given name are the same as the first and last name in any of the names in either list
if one or more matches is found, looks to see if a middle name is present in the given name AND looks to see if a middle name is present in the matches
    Returns (True,True) if there is a middle name in all matches and the given name
    Returns (True,False) if there is a middle name in all matches but no middle name in given name
    Returns (False,True) if there is no middle name in one or more of the matches but a middle name is present in the given name
    Returns (False,False) if there is no middle name in one or more of the matches and no middle name present in the given name
"""
def firstlast(name,list1,list2):
    firstlastL1=list1.copy()
    firstlastL2=list2.copy()
    if len(name.split(' '))>1:
        FL_name=name.split(' ')[0]+' '+name.split(' ')[-1]
    for n in firstlastL1:
        if len(n.split(' '))>1:
            firstlastL1[firstlastL1.index(n)]=n.split(' ')[0]+' '+n.split(' ')[-1]
    for n in firstlastL2:
        if len(n.split(' '))>1:
            firstlastL2[firstlastL2.index(n)]=n.split(' ')[0]+' '+n.split(' ')[-1]
         
    print(firstlastL1)
    print(firstlastL2)
    return
        
nameslist1=['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'isez alba youkshire', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group','ivan young','James sanders', 'ivan albert young', 'isaac young']
nameslist2=['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'isez alba youkshire', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group','ivan young','James sanders', 'ivan albert young', 'isaac young']
firstlast('hello',nameslist1,nameslist2)

#adds names of students who are coming to class this week for the first time to this week's attendance
def getnewnames(weeksfullattendance,masterstudentlist):
    namq=0
    for n in weeksfullattendance:
        weeksfullattendance[weeksfullattendance.index(n)]=weeksfullattendance[weeksfullattendance.index(n)].upper()
    for n in masterstudentlist:
        masterstudentlist[masterstudentlist.index(n)]=masterstudentlist[masterstudentlist.index(n)].upper()
    while namq!='END':
        namq=input("Enter name of new student to add to list. type 'end' when finished").upper()
        while namq.upper() in masterstudentlist or namq.upper() in weeksfullattendance:
            namq=input('sorry but you must enter a unique name for each student. try again').upper()
        if namq!='END':
            weeksfullattendance.append(namq)
            masterstudentlist.append(namq)
    return weeksfullattendance

#make a function which extracts out groups where a particular student was a member
def groupextractor(student_name, prvgroups):
    retlist=[]
    for n in prvgroups:
        if student_name in n:
            retlist.append(n)
    return retlist

#make a function, given a student name, returns a list of all of that student's previous partners
def prevpartnerlistmaker(student_name,prvgroups):
    prev_partners=[y for x in prvgroups if student_name in x for y in x if y!=student_name]
    return prev_partners



"""
make a function which returns a dictionary array of previous partners for each student

"""
def arrayunusedpartners(attendance,prvgroups):
    returndictionary=dict()
    
    for n in attendance:
        shallowcopy=attendance.copy()
        shallowcopy.remove(n)
        prev_partners=[y for x in prvgroups if n in x for y in x if y!=n]
        unusedpartner= [value for value in shallowcopy if value not in prev_partners]
        returndictionary[n]=unusedpartner
    # for key in returndictionary:
    #     print(str(key) +':'+str(returndictionary[key]))
    # input('this is a key for what unused partners each student has left available to choose from')
    return returndictionary

"""
given a list and an item from that list.. check if that item is unique
    return True or False

"""
def unique(lst,item):
    if lst.count(item)>1:
        return False
    elif lst.count(item)==1:
        return True
    else:
        return None

# names=['isaac a young', 'james smith', 'inez alba yorkshire', 'jessica simpson','james smith']
# item1='isaac a young'
# item2='james smith'
# item3='luciana'
# print(unique(names,item1))
# print(unique(names,item2))
# print(unique(names,item3))
"""
given a name and a list of names, finds a set of initials for the name which makes it unique among all other names..
    return the initials that work for that person

for example if given ['isaac a young', 'james arnold smith', 'inez alba yorkshire', 'jessica simpson','james allerton smith', 'james southland', 'james smith', 'luciana Young', 'olivia eve-sa young', 'isabelle A Young','ivan young']
    Returns IsaaAY when name given is 'isaac a young', because isabelle and isaac have the same last name and middle initial
    Returns JArSm when name given is 'james arnold smith' because james arnold smith and james allerton smith have the same first name. Ar used because there are two James Smith in the class with different middle names.
    Returns JSo when name given is 'james smith' because james smith and james southland have the same first name.
    Returns IsabAY when name given is 'isabelle A Young'
    Returns IvY if given 'ivan young' because IY could be missconstrued to be Isaac A Young or isabelle A young since one might not notice that the middle name is just missing in ivan young
"""
def initials(name, namelist):
    simpinitials=''.join(x[0].upper() for x in name.split(' '))
    namelist.remove(name)
    sameinit_non_spCase=namelist.copy()
    noMI_spCase=[]
    sameFN_spCase=[]
    sameLN_spCase=[]
    for n in namelist:
        testinitial=''.join(x[0].upper() for x in n.split(' '))
        if simpinitials!=testinitial:
            sameinit_non_spCase.remove(n)
        if len(testinitial)==2 and testinitial[0]==simpinitials[0] and testinitial[1]==simpinitials[-1] and len(simpinitials)!=2:
            noMI_spCase.append(n)
        if simpinitials==testinitial and name.split(' ')[0].upper()==n.split(' ')[0].upper():
            sameinit_non_spCase.remove(n)
            sameFN_spCase.append(n)
        if simpinitials==testinitial and name.split(' ')[-1].upper()==n.split(' ')[-1].upper():
            sameinit_non_spCase.remove(n)
            sameLN_spCase.append(n)
    input(noMI_spCase)
    input(sameFN_spCase)
    input(sameLN_spCase)
    return sameinit_non_spCase
    # firstname=name.split(' ')[0]
    # lastname=name.split(' ')[:]

# nameslist=['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'isez alba youkshire', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group','ivan young','James sanders', 'ivan albert young', 'isaac young']
# print(initials('isaac a young',nameslist))
"""
given a list of single word name keys (such as list of first names) with letters as items [[key,item],[key1,item1]]
    returns dictionary of names with their shortest unique string..
if given a list of names instead.. first converts it to a Nx2 array..
if two names are identical, sets those to just the first initial
    
    for example: if given James, James, Isaac, Isabelle, Isaac, and Ivan
    the returned dictionary will be [[isaac,Isaa],[isaac,Isaa],[James,J],[James,J],[isabelle,isab],[ivan,iv]]
"""
def nameuniquefinder(names):
    if type(names)==list:
        retdict={}
        for n in names:
            retdict[n]=''
    else:
        retdict=names.copy()
    
    for n in retdict:
        if not unique([retdict[x] for x in retdict],retdict[n]):
            for m in retdict:
                retdict[m]=retdict[m]+m[len(retdict[m]):len(retdict[m])+1]
            
    repeatflag=0
    print([retdict[x] for x in retdict])
    for n in retdict:
        input(f'{n},{retdict[n]}')
        if not unique([retdict[x] for x in retdict],retdict[n]):
            repeatflag=1
    if repeatflag==1:
        retdict=nameuniquefinder(retdict)
    return retdict
# names=['isaac a young', 'james smith', 'inez alba yorkshire', 'jessica simpson','james smith']
# names={'isaac': '', 'james': '', 'inez': '', 'jamsica': '', 'james': ''}
# print(nameuniquefinder(names))

"""
make a function which converts a list of names into unique initials
if two people have identical initials, adds another letter from the first name and last name to each person in identical people
    returns new dictionary that connects each person's name to their initials

"""
def initialsdictionary(names):
    listof_initials={}
    conflict_initials={}
    conflict_initialslist=[]
    conflict_names=[]
    initialsdict={}
    for n in names:
        listof_initials[n]=''.join(x[0].upper() for x in n.split(' '))
    listdict=list(listof_initials.items())
    # input(type(listdict))
    initials=[n[1] for n in listdict]
    count=-1
    for n in initials:
        count+=1
        if initials.count(n)>1:
            print(f'{n} is the initials of {listdict[count]}')
            conflict_initials[listdict[count][0]]=listdict[count][1]
            conflict_initialslist.append(n)
            conflict_names.append(listdict[count][0])
    print(conflict_initials)
    print(conflict_names)
    print(set(conflict_initialslist))
    for n in set(conflict_initialslist):
        nameslist=[]
        for m in conflict_initials:
            if conflict_initials[m]==n:
                nameslist.append(m)
        initialsdict[n]=nameslist
    print(initialsdict)
    # for n in listof_initials:
    #     if listof_initials.item s() and n not in notunique_initials:
    #         notunique_initials.append(n)
    # input(notunique_initials)
    
    # initial_dictionary={}
 
    return
# unused_name_array={'isaac a young': ['james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'isez alba youkshire', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group'], 'james smith': ['isaac a young', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'inez alba yorkshire', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group'], 'nancy': ['isaac a young', 'james smith', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'inez alba yorkshire', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group'], 'olivia eve-sa young': ['isaac a young', 'james smith', 'nancy', 'pedro lopes de sa loureiro', 'inez alba yorkshire', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group'], 'pedro lopes de sa loureiro': ['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'inez alba yorkshire', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group'], 'inez alba yorkshire': ['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group'], 'luciana young': ['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'inez alba yorkshire', 'jessica simpson', 'sam carmichael', 'join another group'], 'jessica simpson': ['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'inez alba yorkshire', 'luciana young', 'sam carmichael', 'join another group'], 'sam carmichael': ['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'inez alba yorkshire', 'luciana young', 'jessica simpson', 'join another group'], 'join another group': ['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'inez alba yorkshire', 'luciana young', 'jessica simpson', 'sam carmichael']}
# nameslist=['isaac a young', 'james smith', 'nancy', 'olivia eve-sa young', 'pedro lopes de sa loureiro', 'isez alba youkshire', 'luciana young', 'jessica simpson', 'sam carmichael', 'join another group']
# initialsconversion=initialsdictionary(nameslist)
# print([n for n in initialsconversion])
# 
"""
make a function that returns conflict keys from a dictionary of unused partners
IE if both a and b need to pair with d, then report back that either a or b will need to be moved to the orphan list
and furthermore if a, b, and c need to pair with d and e.. then one of a, b, or c will need to move to the orphan list since there are only 2 options available for 3 students in need.
similar logic follows for any group of n people who need to be paired up with n-1 people.
    return a list of students randomly selected who will move to the orphan ilst in order for it to work out
"""
def conflictremover(unused_partner_dict):
    import random
    retlist=[]
    ultretlist=[]
    for key in unused_partner_dict:
        conflictees=[k for k,v in unused_partner_dict.items() if v == unused_partner_dict[key]]
        if len(conflictees)>len(unused_partner_dict[key]) and set(conflictees) not in [x[1] for x in retlist]:
            retlist.append([len(unused_partner_dict[key]),set(conflictees)])
    for n in retlist:
        input(f'there were conflicts that needed to be resolved. students: {n[1]} only had {n[0]} legal partner to fight over.')
    # input(retlist)
    for n in retlist:
        templist=list(n[1])
        while len(templist)>=n[0]:
            neworphan=random.choice(templist)
            ultretlist.append(neworphan)
            templist.remove(neworphan)
            n[0]+=1
    return ultretlist
# prvgroups_lists=[ ['a', 'b'], ['a', 'c'],  ['a', 'e'], ['a', 'f'], ['a', 'g'], ['a', 'h'], ['b', 'c'],  ['b', 'e'], ['b', 'f'], ['b', 'g'], ['b', 'h'], ['c', 'h'], ['c', 'e'], ['c', 'f'], ['c', 'g'], ['d', 'e'], ['d', 'f'], ['e', 'f']]
# attendance=['a', 'b', 'c', 'd', 'e', 'f', 'g','h']
# prvgroups_2_ppl=[ ['a', 'b'], ['a', 'c'],  ['a', 'e'], ['a', 'f'], ['a','d'], ['b', 'c'],  ['b', 'e'], ['b', 'f'], ['b', 'g'], ['b', 'h'], ['c', 'h'], ['c', 'e'], ['c', 'f'], ['c', 'g'], ['d', 'e'], ['d', 'f'], ['e', 'f'],['i','a'],['i','b'],['i','c'],['i','d'],['i','e'],['i','f']]
# attendance=['a', 'b', 'c', 'd', 'e', 'f', 'g','h','i']
# arrstuprevpartners=arrayunusedpartners(attendance, prvgroups_2_ppl)
# for key in arrstuprevpartners:
#     print(key,':',arrstuprevpartners[key])
# input('pressentertocont')
# print(conflictremover(arrstuprevpartners))


"""
make a function which takes attendance list and list of previous groups 
    returns: list of orphans with no possible partners.

"""
def orphans(attendance,prvgroups):
    orphans=[]
    students_avail_partners=arrayunusedpartners(attendance,prvgroups)
    for n in students_avail_partners:
        if len(students_avail_partners[n])==0:
            orphans.append(n)
    return orphans
# attendance=['a', 'b', 'c', 'd', 'e', 'f', 'g','h']
# prvgroups_no_orphans=[ ['a', 'b'], ['a', 'c'],  ['a', 'e'], ['a', 'f'], ['a', 'g'], ['a', 'h'], ['b', 'c'],  ['b', 'e'], ['b', 'f'], ['b', 'g'], ['b', 'h'], ['c', 'h'], ['c', 'e'], ['c', 'f'], ['c', 'g'], ['d', 'e'], ['d', 'f'], ['e', 'f']]
# prvgroups_1_orphan= [ ['a', 'b'], ['a', 'c'],  ['a', 'e'], ['a', 'f'], ['a', 'g'], ['a', 'h'], ['a', 'd'],  ['b', 'e'], ['b', 'f'], ['b', 'g'], ['b', 'h'], ['c', 'h'], ['c', 'e'], ['c', 'f'], ['c', 'g'], ['d', 'e'], ['d', 'f'], ['e', 'f']]
# prvgroups_2_orphan=[ ['a', 'b'], ['a', 'c'],  ['a', 'e'], ['a', 'f'], ['a', 'g'], ['a', 'h'], ['a', 'd'],  ['b', 'e'], ['b', 'f'], ['b', 'g'], ['b', 'h'], ['b', 'c'], ['b', 'd'], ['c', 'f'], ['c', 'g'], ['d', 'e'], ['d', 'f'], ['e', 'f']]
# print(orphans(attendance,prvgroups_no_orphans))
# print(orphans(attendance,prvgroups_1_orphan)) #student a is an orphan
# print(orphans(attendance,prvgroups_2_orphan)) #student b and student a are orphans
"""
make a function which uses attendance list and list of previous group pairings and returns
    list of groupings which are forced because the student has only one possible partner

"""

def forcedpartners(attendance,prvgroups):
    forcedgroups=[]
    students_avail_partners=arrayunusedpartners(attendance,prvgroups)
    for n in students_avail_partners:
        if len(students_avail_partners[n])==1:
            forcedgroups.append([n,students_avail_partners[n][0]])
    # print(forcedgroups)
    # for n in attendance:
    #     shallowcopy=attendance.copy()
    #     shallowcopy.remove(n)
    #     prev_partners=[y for x in prvgroups if n in x for y in x if y!=n]
    #     if len(shallowcopy)-1==len(prev_partners):
    #         unusedpartner= [value for value in shallowcopy if value not in prev_partners]
    #         partnership=[n,unusedpartner[0]]
    #         # if partnership in forcedgroups or [partnership[1],partnership[0]] in forcedgroups:
    #             # print(F"possible in RG.forcedpartners()?? the proposed partnership: {partnership} forced group already found in a previous iteration: {forcedgroups}")
    #         if partnership not in forcedgroups and [partnership[1],partnership[0]] not in forcedgroups:
    #             # print('looks like we have a student who has only one possible partner! student ***' + str(n) +'*** must go with student ***' +   str(unusedpartner[0])+'***')
    #             forcedgroups.append(partnership)
    
    return forcedgroups

#test data below:
# attendance=['a', 'b', 'c', 'd', 'e', 'f', 'g','h']
# prvgroups_lists=[ ['a', 'b'], ['a', 'c'],  ['a', 'e'], ['a', 'f'], ['a', 'g'], ['a', 'h'], ['b', 'c'],  ['b', 'e'], ['b', 'f'], ['b', 'g'], ['b', 'h'], ['c', 'h'], ['c', 'e'], ['c', 'f'], ['c', 'g'], ['d', 'e'], ['d', 'f'], ['e', 'f']]
# print(forcedpartners(attendance,prvgroups_lists))

"""
***unused function: this was upgraded to conflictremover to deal with any conflicts even if 10 different students all need the same batch of 9 students.  

make a function which determines if there are conflicts where 1 student is pulled towards multiple partners who all NEED that one partner
randomly chooses who is now stuck as an orphan this week because their only possible partner is already taken that conflict to one of the possible partnerships

    returns a list of students who are now orphans

"""
def conflictresolver(forcedgroups):
    import random
    neworphans=[]
    problempeople=[]
    
    partners1=[x[1] for x in forcedgroups]
    partners2=[x[0] for x in forcedgroups]
    allstu=partners1+partners2
    for x in allstu:
        if allstu.count(x)>1 and x not in problempeople:
            problempeople.append(x)
    for n in problempeople:
        victims=[y for x in forcedgroups if n in x for y in x if y!=n]
        luckystudent=victims[random.randrange(len(victims))]
        victims.remove(luckystudent)
        neworphans+=victims
        
        

    input(f'these are the unlucky students who must go with a new partner because of another student: {neworphans}')
    return neworphans
# conflictresolver([['a', 'd'], ['b', 'd'], ['c', 'h'], ['g', 'h'], ['e', 'h']])

"""
make a function that removes the conflicted groups from a list of forced groups, uses data returned from conflictresolver
    returns a list of forced groups that are still valid.

"""
def forcedpartners_trimmer(neworphans,forcedgroups):
    newforcedgroups=[x for x in forcedgroups if x[0] not in neworphans and x[1] not in neworphans]
    # print(newforcedgroups)
    return newforcedgroups

# neworphans=conflictresolver([['a', 'd'], ['b', 'd'], ['c', 'h'], ['g', 'h'], ['e', 'h']])
# forcedpartners_trimmer(neworphans,[['a', 'd'], ['b', 'd'], ['c', 'h'], ['g', 'h'], ['e', 'h']])

"""
a can only go with d 
but b can only go with d as well
so there is a conflict and only a coin toss can decide who gets to go with d

the student who loses the coin toss is therefore an orphan and must find a repeat partner. IE they join the orphans list.

C is a singlet (can only pair with h)

student d can go with g, h, a, or b

and e is a doublet (can only pair with g or h)


"""
prvgroups_tuples=[ ('a', 'c'),('a', 'b'), ('d', 'a'), ('a', 'e'), ('a', 'f'), ('a', 'g'), ('a', 'h'), ('b', 'c'), ('b', 'd'), ('b', 'e'), ('b', 'f'), ('b', 'g'), ('b', 'h'), ('c', 'd'), ('c', 'e'), ('c', 'f'), ('c', 'g'), ('d', 'e'), ('d', 'f')]
prvgroups_lists=[ ['a', 'b'], ['a', 'c'],  ['a', 'e'], ['a', 'f'], ['a', 'g'], ['a', 'h'], ['b', 'c'],  ['b', 'e'], ['b', 'f'], ['b', 'g'], ['b', 'h'], ['c', 'd'], ['c', 'e'], ['c', 'f'], ['c', 'g'], ['d', 'e'], ['d', 'f'], ['e', 'f']]
attendance=['a', 'b', 'c', 'd', 'e', 'f', 'g','h']
# attendance.remove('b')
# print(attendance)
# print(type(attendance))
# print(orphans(attendance,prvgroups_lists))
# print(forcedpartners(attendance,prvgroups_lists))
def simp(stuname, group):
    if stuname in group:
        return(group)
    else:
        return 
# newlist=[x for i in prvgroups_lists if x !='a']

# print(newlist)
# newlist=[simp('a',n) for n in prvgroups_lists if simp('a',n)!=None]
# newlist.remove(None)
# print(str(newlist))
# stuofint='h'
# print(str([y for x in prvgroups_lists if stuofint in x for y in x if y!=stuofint]))
# lista=['b', 'c', 'd', 'e', 'f', 'g', 'h']
# listb=['c', 'b', 'd', 'e', 'f', 'g', 'h']

# print(set(lista)==set(listb))

# prevgroups=[['g', 'd'], ['f', 'c'], ['e', 'b'], ['a', 'join another group'], ['f', 'join another group'], ['a', 'g'], ['b', 'c'], ['e', 'd'], ['a', 'e'], ['d', 'join another group'], ['b', 'f'], ['c', 'g'], ['a', 'f'], ['e', 'c'], ['d', 'b'], ['a', 'd'], ['g', 'b'], ['join another group', 'c'], ['f', 'e'], ['c', 'd'], ['g', 'f'], ['e', 'join another group'], ['b', 'a'], ['f', 'd'], ['c', 'a'], ['join another group', 'b'], ['g', 'e'], ['7', 'c'], ['8', 'f'], ['3', '2'], ['6', 'b'], ['join another group', 'g'], ['5', 'a'], ['e', '1'], ['4', 'd'], ['1', 'join another group'], ['f', '7'], ['e', '2'], ['d', '3'], ['g', '8'], ['b', '5'], ['a', '4'], ['c', '6'], ['e', '5'], ['g', '6'], ['1', 'c'], ['b', '4'], ['join another group', '8'], ['f', '3'], ['d', '2'], ['a', '7'], ['4', 'e'], ['c', '8'], ['7', 'join another group'], ['5', 'g'], ['6', 'a'], ['1', 'd'], ['2', 'f'], ['3', 'b'], ['6', 'f'], ['8', 'e'], ['4', 'c'], ['5', 'd'], ['join another group', '2'], ['7', 'b'], ['3', 'g'], ['1', 'a'], ['3', 'join another group'], ['d', '7'], ['b', '1'], ['2', 'c'], ['e', '6'], ['a', '8'], ['f', '5'], ['g', '4'], ['8', 'b'], ['7', 'g'], ['6', 'd'], ['a', '2'], ['1', 'f'], ['join another group', '4'], ['3', 'e'], ['5', 'c'], ['8', '5'], ['2', '7'], ['3', '4'], ['join another group', '6'], ['8', '1'], ['4', '5'], ['6', '2'], ['3', '7']]

# attendance=['a', 'b', 'c', 'd', 'e', 'f', 'g', '1', '2', '3', '4', '5', '6', '7', '8','join another group']


"""
        2. group of pairs of all those students who have only 1 possible partner
        3. lsit of students remaining who have not been paired.
"""