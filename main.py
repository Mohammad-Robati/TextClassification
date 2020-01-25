import math
# HAM-Train-Test/HAM-Train.txt
def calculateUnigramModel(file):
    docClasses = {}
    docClassOccuringCounts = {}
    allCount = 0
    with open(file, 'r') as f:
        for line in f:
            words = line.split()
            docClass = ''
            allCount += 1
            for i in range(len(words)):
                if words[i] == 'ادب' and words[i+1] == 'و' and words[i+2] == 'هنر@@@@@@@@@@':
                    docClass = 'ادب و هنر@@@@@@@@@@'
                    if docClass in docClassOccuringCounts:
                        docClassOccuringCounts[docClass] += 1
                    else:
                        docClassOccuringCounts[docClass] = 1
                    continue
                if '@' in words[i] and docClass == '':
                    docClass = words[i]
                    if docClass in docClassOccuringCounts:
                        docClassOccuringCounts[docClass] += 1
                    else:
                        docClassOccuringCounts[docClass] = 1
                    continue
                if docClass not in docClasses:
                    docClasses[docClass] = {}
                key = words[i]
                if key in docClasses[docClass]:
                    docClasses[docClass][key] += 1
                else:
                    docClasses[docClass][key] = 1
    probabilities = {}
    for docClass in docClasses:
        docClassProbability = {}
        for word in docClasses[docClass]:
            docClassProbability[word] = docClasses[docClass][word] / len(docClasses[docClass])
        probabilities[docClass] = docClassProbability
    classProbability = {}
    for docClass in docClassOccuringCounts:
        classProbability[docClass] = docClassOccuringCounts[docClass] / allCount
    return docClasses, probabilities


def calculateBigramModel(file):
    uniCounts = calculateUnigramModel(file)[0]
    docClasses = {}
    docClassOccuringCounts = {}
    allCount = 0
    with open(file, 'r') as f:
        for line in f:
            words = line.split()
            docClass = ''
            allCount += 1
            for i in range(len(words)):
                if words[i] == 'ادب' and words[i+1] == 'و' and words[i+2] == 'هنر@@@@@@@@@@':
                    docClass = 'ادب و هنر@@@@@@@@@@'
                    if docClass in docClassOccuringCounts:
                        docClassOccuringCounts[docClass] += 1
                    else:
                        docClassOccuringCounts[docClass] = 1
                    continue
                if '@' in words[i] and docClass == '':
                    docClass = words[i]
                    if docClass in docClassOccuringCounts:
                        docClassOccuringCounts[docClass] += 1
                    else:
                        docClassOccuringCounts[docClass] = 1
                    continue
                if docClass not in docClasses:
                    docClasses[docClass] = {}
                key = words[i-1] + ' ' + words[i]
                if key in docClasses[docClass]:
                    docClasses[docClass][key] += 1
                else:
                    docClasses[docClass][key] = 1
    probabilities = {}
    for docClass in docClasses:
        docClassProbability = {}
        for biwords in docClasses[docClass]:
            [first, second] = biwords.split()
            if '@' not in first and 'ادب' not in first:
                docClassProbability[biwords] = docClasses[docClass][biwords] / uniCounts[docClass][first]
        probabilities[docClass] = docClassProbability
    classProbability = {}
    for docClass in docClassOccuringCounts:
        classProbability[docClass] = docClassOccuringCounts[docClass] / allCount
    return probabilities, classProbability


def testBigram(file, testFile):
    probabilities, classProbability = calculateBigramModel(file)
    finalResults = []
    with open(testFile, 'r') as f:
        for line in f:
            maxP = ['', '', 0]
            realDocClass = ''
            for docClass in probabilities:
                calculatedProbability = 0
                words = line.split()
                for i in range(len(words)):
                    if words[i] == 'ادب' and words[i + 1] == 'و' and words[i + 2] == 'هنر@@@@@@@@@@':
                        continue
                    if '@' in words[i]:
                        if words[i] == 'هنر@@@@@@@@@@':
                            realDocClass = 'ادب و هنر@@@@@@@@@@'
                            continue
                        realDocClass = words[i]
                        continue
                    key = words[i - 1] + ' ' + words[i]
                    if key in probabilities[docClass]:
                        calculatedProbability += math.log2(probabilities[docClass][key])
                    else:
                        pass
                calculatedProbability += math.log2(classProbability[docClass])
                if calculatedProbability < maxP[2]:
                    maxP = [docClass, realDocClass, calculatedProbability]
            finalResults.append(maxP)
    return finalResults

def calculatePrecisionAndRecall(results):
    stats = {}
    precision = {}
    recall = {}
    for result in results:
        if result[1] == result[0]:
            if result[1] not in stats:
                stats[result[1]] = {'true': 0, 'false': 0}
                stats[result[1]]['true'] = 1
            else:
                stats[result[1]]['true'] += 1
        else:
            if result[1] not in stats:
                stats[result[1]] = {'true': 0, 'false': 0}
                stats[result[1]]['false'] = 1
            else:
                stats[result[1]]['false'] += 1
    for stat in stats:
        precision[stat] = (stats[stat]['true'] / (stats[stat]['true'] + stats[stat]['false'])) * 100
    for result in results:
        if result[0] == result[1]:
            if result[0] not in stats:
                stats[result[0]] = {'true': 0, 'false': 0}
                stats[result[0]]['true'] = 1
            else:
                stats[result[0]]['true'] += 1
        else:
            if result[0] not in stats:
                stats[result[0]] = {'true': 0, 'false': 0}
                stats[result[0]]['false'] = 1
            else:
                stats[result[0]]['false'] += 1
    for stat in stats:
        recall[stat] = (stats[stat]['true'] / (stats[stat]['true'] + stats[stat]['false'])) * 100
    print(precision)
    print(recall)

# x = testBigram('HAM-Train-Test/HAM-Train.txt', 'HAM-Train-Test/HAM-Test.txt')
x = testBigram('HAM-Train-Test/mytrain.txt', 'HAM-Train-Test/mytest.txt')
calculatePrecisionAndRecall(x)