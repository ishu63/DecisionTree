# Coded by: Ishita Patel (ishitanp@usc.edu)

import re
import math
import copy


def input_data(file):
    words = file.readline()
    words = file.readline()
    words = [re.split(';\n|, | |;', line) for line in file.readlines()]
    for list in words:
        del list[0]
        del list[-1]
    return words


def print_2dlist(list2d):
    for line in list2d:
        print line


def calc_inp(n,p):
    Inp = -(1.0/(n+p))*(p*math.log(p) + n*math.log(n) - (n+p)*math.log(n+p))
    return Inp


def majority(data, column_names, predict):
    index = column_names.index(predict)
    freq = {}
    for tuple in data:
        if (freq.has_key(tuple[index])):
            freq[tuple[index]] += 1
        else:
            freq[tuple[index]] = 1
    max = 0
    major = ""
    for key in freq.keys():
        if freq[key] > max:
            max = freq[key]
            major = key
    return major


def entropy(column_names, data, predict):
    freq = {}
    i = column_names.index(predict)
    for entry in data:
        if (freq.has_key(entry[i])):
            freq[entry[i]] += 1.0
        else:
            freq[entry[i]] = 1.0
    dataEntropy = 0.0
    for freq1 in freq.values():
        dataEntropy += (-freq1 / len(data)) * (math.log(freq1, 10) - math.log(len(data), 10))
    return dataEntropy


def Info_gain(column_names, data, attr, predict):
    valFreq = {}
    subsetEntropy = 0.0
    i = column_names.index(attr)
    for entry in data:
        if (valFreq.has_key(entry[i])):
            valFreq[entry[i]] += 1.0
        else:
            valFreq[entry[i]] = 1.0
    for val in valFreq.keys():
        valProb = float( valFreq[val] / sum(valFreq.values()) )
        dataSubset = [entry for entry in data if entry[i] == val]
        subsetEntropy += valProb * entropy(column_names, dataSubset, predict)
    ret_val = (entropy(column_names, data, predict) - subsetEntropy)
    return ret_val


def findbest(data, column_names, predict):
    best = column_names[0]
    maxGain = 0
    for attr in column_names:
        if not attr == predict:
            newGain = Info_gain(column_names, data, attr, predict)
            if newGain > maxGain:
                maxGain = newGain
                best = attr
    return best


def getValues(data, column_names, column):
    values = []
    index = column_names.index(column)
    for list in data:
        if list[index] not in values:
            values.append(list[index])
    return values


def getExamples(data, column_names, best_column, val):
    index = column_names.index(best_column)
    examples = []
    for list in data:
        if list[index] == val:
            newEntry = []
            for i in range(0, len(list)):
                if i != index:
                    newEntry.append(list[i])
            examples.append(newEntry)
    return examples


def GenerateTree(data, column_names, predict):
    data = data[:]
    can_predict = [values[column_names.index(predict)] for values in data]
    predict_default = majority(data, column_names, predict)
    # no data or only one attribute to select then return predict_default
    if not data or (len(column_names)) <= 1:
        return predict_default
    # found pure class
    elif can_predict.count(can_predict[0]) == len(can_predict):
        return can_predict[0]
    else:
        best_column = findbest(data, column_names, predict)
        tree = {best_column:{}}
        for val in getValues(data, column_names, best_column):
            newAttr = column_names[:]
            newAttr.remove(best_column)
            examples = getExamples(data, column_names, best_column, val)
            subtree = GenerateTree(examples, newAttr, predict)
            tree[best_column][val] = subtree
    return tree


def print_tree(tree,recursion):
    for node in tree:
        for i in range(0,recursion):
            print "\t",
        print node + ':'
        if isinstance(tree[node], dict):
            print_tree(tree[node], recursion+1)
        else:
            for i in range(0,recursion+2):
                print "\t",
            print "Will Enjoy?: \"" + tree[node] + "\""


def find_sol(tree, query):
    new_tree = copy.deepcopy(tree)
    if not isinstance(new_tree, dict):
        return new_tree
    else:
        for node in new_tree:
            new_tree = new_tree[node]
            new_tree = new_tree[query[node]]
            sol = find_sol(new_tree, query)
    return sol


column_names = ["Occupied", "Price", "Music", "Location", "VIP", "Favorite Beer", "Enjoy"]
attribute = {}
datafile = open("dtdata.txt", "r")
data = input_data(datafile)
print_2dlist(data)

predict = "Enjoy"
tree = GenerateTree(data, column_names, predict)
print_tree(tree,0)

query = {"Occupied":'Moderate', "Price":'Cheap', "Music":'Loud', "Location":'City-Center', "VIP":'No', "Favorite Beer":'No'}
print 'Query: ',
print query
sol = find_sol(tree, query)
print 'Will Enjoy?: ',
print sol

datafile.close()
