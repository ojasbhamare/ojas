from sys import *
from csv import reader, DictReader

if len(argv) != 3:
    print("python dna.py data.csv sequence.txt")
    exit()

with open(argv[2]) as file:
    file_reader = reader(file)
    for row in file_reader:
        d_list = row

dna = d_list[0]

sequences = {}

with open(argv[1]) as p_file:
    people_reader = reader(p_file)
    for row in people_reader:
        dnaSequences = row
        dnaSequences.pop(0)
        break

for item in dnaSequences:
    sequences[item] = 1

for key in sequences:
    l = len(key)
    tempMax = 0
    temp = 0
    for i in range(len(dna)):
        while temp > 0:
            temp -= 1
            continue

        if dna[i: i + l] == key:
            while dna[i - l: i] == dna[i: i + l]:
                temp += 1
                i += l

            if temp > tempMax:
                tempMax = temp

    sequences[key] += tempMax

with open(argv[1], newline='') as peoplefile:
    people = DictReader(peoplefile)
    for person in people:
        match = 0
        for dna in sequences:
            if sequences[dna] == int(person[dna]):
                match += 1
        if match == len(sequences):
            print(person['name'])
            exit()
    print("No match")