import csv

data1 = list(csv.reader(open("SourceCmp/Source1.csv")))
data2 = list(csv.reader(open("SourceCmp/Source2.csv")))

def genKey(infoarr, intarr=[0, 1, 2, 3, 4]):
    # intarr is a list of ints which are used to create the key
    keyarr = []
    for i in intarr:
        keyarr.append(infoarr[i])
    return tuple(keyarr)

def genValue(infoarr, intarr=[5, 6]):
    # intarr is a list of ints which are used to create the value
    valarr = []
    for i in intarr:
        valarr.append(infoarr[i])
    return valarr

def sourcecmp(source1, source2, compfn):
    locationdict = {} # dictionary of key locations
    valuedict = {} # dictionary of value associations
    # loop through first source
    for i in range(len(source1)):
        key = genKey(source1[i])
        value = genValue(source1[i])
        if key not in locationdict:
            locationdict[key] = [[i+1], []]
            valuedict[key] = [[value], []]
        else:
            locationdict[key][0].append(i+1)
            valuedict[key][0].append(value)
    # loop through second source
    for i in range(len(source2)):
        key = genKey(source2[i])
        value = genValue(source2[i])
        if key not in locationdict:
            locationdict[key] = [[], [i+1]]
            valuedict[key] = [[], [value]]
        else:
            locationdict[key][1].append(i+1)
            valuedict[key][1].append(value)
    # filter valuedict for keys which appear in both source1 and source2
    valuedict = {k:v for k,v in valuedict.items() if len(v[0]) > 0 and len(v[1]) > 0}
    for k in valuedict:
        for a in range(len(valuedict[k][0])):
            for b in range(len(valuedict[k][1])):
                if compfn(valuedict[k][0][a], valuedict[k][1][b]):
                    print(f"Source 1 Row {locationdict[k][0][a]} and Source 2 Row {locationdict[k][1][b]} matches comparison function")

sourcecmp(data1, data2, lambda a, b: a == b)
