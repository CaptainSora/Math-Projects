import csv

SEP = 5

data1 = list(csv.reader(open("SourceCmp/Source1.csv")))
data2 = list(csv.reader(open("SourceCmp/Source2.csv")))

def sourcecmp(source1, source2, compfn):
    locationdict = {}
    valuedict = {}
    for i in range(len(source1)):
        if tuple(source1[i][:SEP]) not in locationdict:
            locationdict[tuple(source1[i][:SEP])] = [[i+1], []]
            valuedict[tuple(source1[i][:SEP])] = [[source1[i][SEP:]], []]
        else:
            locationdict[tuple(source1[i][:SEP])][0].append(i+1)
            valuedict[tuple(source1[i][:SEP])][0].append(source1[i][SEP:])

    for i in range(len(source2)):
        if tuple(source2[i][:SEP]) not in locationdict:
            locationdict[tuple(source2[i][:SEP])] = [[], [i+1]]
            valuedict[tuple(source2[i][:SEP])] = [[], [source2[i][SEP:]]]
        else:
            locationdict[tuple(source2[i][:SEP])][1].append(i+1)
            valuedict[tuple(source2[i][:SEP])][1].append(source2[i][SEP:])

    # check if valuedict both arrays are nonempty
    # nonempty(array) fn might be faster
    vd = {k:v for k,v in valuedict.items() if len(v[0]) > 0 and len(v[1]) > 0}
    for k in vd:
        for a in range(len(vd[k][0])):
            for b in range(len(vd[k][1])):
                if compfn(vd[k][0][a], vd[k][1][b]):
                    print(f"Source 1 Row {locationdict[k][0][a]} and Source 2 Row {locationdict[k][1][b]} matches comparison function")

sourcecmp(data1, data2, lambda a, b: a == b)
