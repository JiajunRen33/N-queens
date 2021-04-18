#Group 7
import random


# Implement a solver that returns a list of queen's locations
#  - Make sure the list is the right length, and uses the numbers from 0 .. BOARD_SIZE-1
def solve(board_size):

    
    time = 1
    while time <= 10:
        answer = mini_conf(board_size,10000)
        if answer == []:
            time =time+ 1
        else:
            print(answer)
            return(answer)
    return "fail"




def maping(n):# To form a random matrix with no Q on each row and column then count the number of Qs on each diagnal and get location of Qs
    loc = [-1] * n #loc[x] = y means there is a Q on row x colunm y
    rldiag = [0] * ((2*n)-1) #number of Qs on right to left diagnal
    lrdiag = [0] * ((2*n)-1) #number of Qs on left to right diagnal
    listA = []
    notfound = []
    for k in range(n):
        listA.append(k) # listA is a list has [0,1,2,3....n-1]
    for i in range(n):

        flag = False
        for j in range(len(listA)):
            x = random.sample(listA,1)
            temp = x[0]
            if (rldiag[i+temp] == 0) and (lrdiag[i+n-1-temp] == 0):
                flag = True
                loc[i] = temp
                listA.remove(temp)
                rldiag[i+temp] = 1
                lrdiag[i+n-1-temp] = 1
                break
        if flag == False:
            notfound.append(i)
    for h in notfound:
        x = random.sample(listA,1)
        temp = x[0]
        listA.remove(temp)# get a ramdom number within 0 and n-1 and remove it from listA to avoid getting repetitive number next time
        loc[h] = temp 
        rldiag[h+temp] += 1
        lrdiag[h+((n-1)-temp)] += 1

    return [loc, n*[1] ,rldiag, lrdiag]

def mini_conf(n,maxstep):
    #get the inital location of queens
    map_list = maping(n)
    loc = map_list[0]
    col_num = map_list[1]#number of queens in each col
    rldiag = map_list[2]
    lrdiag = map_list[3]
    #haveconf:cols which have conflit, failnumber is the number of conflict the queen have
    conf = countingfailure([loc, [1]*len(loc), rldiag, lrdiag])
    haveconf = conf[0]
    failnumber = conf[1]
    counter = 1
    success = True
    #stay in loop until we find the solution
    while haveconf != []:
        maxconflist =[]
        #max number of fail
        maxconf = max(failnumber)
        for i in range(len(haveconf)):
            if failnumber[i] == maxconf:
                #find all the index of the fails
                maxconflist.append(haveconf[i])
        random.shuffle(maxconflist)
        #choose one row with most conflict
        row = maxconflist.pop()
        #conflict time in a random col
        eachcol_conf = []
        current_conf = []
        lowest_conf = float("inf")
        for colpos in range(n):
            #for number in a random col, initialize 0,
            #then add conflicts in vertical way and diagonal way
            eachcol_conf.append(0)
            eachcol_conf[colpos] = col_num[colpos]+ rldiag[row + colpos]+lrdiag[row + ((len(loc)-1) - colpos)]

            #find lowest conflicts
            if eachcol_conf[colpos] < lowest_conf:
                current_conf = []
                lowest_conf = eachcol_conf[colpos]
            #may more than one lowest conflict
        for colpos in range(n):
            if eachcol_conf[colpos] == lowest_conf:
                current_conf.append(colpos)
     
        #choose one lowest conflict randomly
        random.shuffle(current_conf)
        #swap: the position of the chosen lowest conflict 
        swap = current_conf.pop()
        
        #the col of wrong one we need to change
        colpos = loc[row]
        
        #the queen comes here so add relative conflicts
        col_num[swap] += 1
        rldiag[row + swap] += 1
        lrdiag[row + ((len(loc)-1) - swap)] += 1
        #the queen in colpos is not exist so remove relative conlicts
        col_num[colpos] -= 1
        rldiag[row + colpos] -= 1
        lrdiag[row + ((len(loc)-1) - colpos)] -= 1

        #change col number in place
        loc[row] = swap
        if counter < maxstep:
            conf = countingfailure([loc, col_num, rldiag, lrdiag])
            haveconf = conf[0]
            failnumber = conf[1]
        else:
            success = False
            break
        counter += 1
        
    if success: #there is a solution
        for i in range(n):
             loc[i] = loc[i] + 1
        return loc
    else: #no solution
        return []
        
def countingfailure(list):
    #Returns a list with all elements currently experiencing mcf
    loc = list[0]
    vertical = list[1]
    rldiag = list[2]
    lrdiag = list[3]
    n = len(loc)
    mconflict = []
    confnum = []

    for row in range(n):
        col = loc[row]
        if (vertical[col] > 1) or (rldiag[row + col] > 1) or (lrdiag[row + ((n-1) - col)] > 1):
            mconflict.append(row)
            #count all the fail times
            failnum = vertical[row] +  rldiag[row + col] + lrdiag[row + ((n-1) - col)]
            confnum.append(failnum)
    return [mconflict,confnum]
 
