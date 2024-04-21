"""
This exercise inputs a dictionary of {"people":[list-of-can-do-tasks]},
outputs the person-tasks assigned in maximum matching, i.e., most people 
doing tasks and most tasks get done.
"""

# reverse the dict to reversedDict
def reverse(dict):
    valueList=[]
    keyList=[]
    reverseD={}
    for d in dict:
        val=dict[d]
        valueList += val
        keyList += d*len(val)

    for i in range(len(valueList)):
        try:
            reverseD[valueList[i]]+=keyList[i]
        except:
            reverseD[valueList[i]]=keyList[i]
    
    print(f"reversedDict:{reverseD}")
    return reverseD

def alloc(dict, values, allocd, lastPair):
    if len(dict)==0 or len(values)==0:
        return allocd

    d=dict.copy()
    v=values.copy()
 
    k1st=list(d.keys())[0]
    if len(lastPair)>0:
        try:
            d[k1st].remove(lastPair[1])
        except:
            pass
        
    if len(d[k1st])>0:
        v1st=d[k1st][0]
    else:
        v1st='*'

    del d[k1st]
    if v1st in v:
        v.remove(v1st)
    else:
        v1st='*'
    
    allocd=alloc(d, v, allocd, (k1st,v1st))
    return allocd + [(k1st,v1st)]

def resolve_free(freeVal, assigned, reversedDict):
    rAssign=[]
    
    # assign that value looking up reversedDict

    rKey=reversedDict[freeVal][0]
    rAssign=[(rKey,freeVal)]

    # look for rVal looking up assigned from rKey
    rVal=0
    for it in assigned:
        if it[0]==rKey:
            rVal=it[1]

    # if there is rVal found take all keys
    if rVal>0:
        for v in reversedDict[rVal]:
            rAssign+=[(v,rVal)]
            if v!=rKey:
                break

    assigned+=rAssign
    print("resolve free:",assigned)
    
    resolved=[]
    for f in assigned:
        if assigned.count(f)==1 and f[1]!='*':
             resolved.append(f)

    print("resolved:",resolved)
    return resolved

def assign_key_val(dict):
    reversedDict=reverse(dict)
    
    allocd=[]
    pair=()
    values=list(reversedDict.keys())

    assigned=alloc(dict, values, allocd, pair)
    print("first alloc:",assigned)

    assignedList=list(zip(*assigned))[1]
    freeValue=list(set(values)-set(assignedList))
    #for freeVal in freeValue:
    freeVal=freeValue[0]
    print("freeVal:",freeVal)
    assigned=resolve_free(freeVal, assigned, reversedDict)

    return assigned

# run for four examples
inputDict = [ { "A": [1,2,3,4], "B": [1], "C":[2], "D":[2,3,4] },
              { "A": [1,2,3,4], "B": [1], "C":[1], "D":[1] },
              { "A": [1,2,3,4,5], "B": [1], "C":[1], "D":[5] },
              { "A": [1,2,3,4], "B": [1,2,3,4], "C":[1,2,3,4] } ]

for inD in inputDict:
    print("input:",inD)
    assign_key_val(inD)
    print("\n")