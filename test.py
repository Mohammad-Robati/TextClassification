import math


class TestModel:

    def __init__(self, testFile):
        self.testFile = testFile

    def testModel(self, model):
        probabilities, classProbability = model
        finalResults = []
        with open(self.testFile, 'r') as f:
            for line in f:
                maxP = ['', '', 0]
                for docClass in probabilities:
                    calculatedProbability = 0
                    pivot = line.find('@')
                    realDocClass = line[0:pivot]
                    words = line[pivot + 10:].split()
                    for i in range(len(words)):
                        key = words[i-1] + ' ' + words[i]
                        if key in probabilities[docClass]:
                            calculatedProbability += probabilities[docClass][key]
                        else:
                            pass
                    calculatedProbability += math.log2(classProbability[docClass])
                    if calculatedProbability < maxP[2]:
                        maxP = [docClass, realDocClass, calculatedProbability]
                finalResults.append(maxP)
            for r in finalResults:
                print(r)
        return finalResults

