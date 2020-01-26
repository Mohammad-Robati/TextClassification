import math


class TrainModel:

    def __init__(self, trainFile, unigramFactor, bigramFactor):
        self.trainFile = trainFile
        self.unigramFactor = unigramFactor
        self.bigramFactor = bigramFactor

    def calculateModel(self):
        unigramDocClasses = {}
        bigramDocClasses = {}
        docClassOccuringCounts = {}
        allCount = 0
        with open(self.trainFile, 'r') as f:
            for line in f:
                allCount += 1
                pivot = line.find('@')
                docClass = line[0:pivot]
                words = line[pivot + 10:].split()
                words.append('SS')
                if docClass in docClassOccuringCounts:
                    docClassOccuringCounts[docClass] += 1
                else:
                    docClassOccuringCounts[docClass] = 1
                for i in range(len(words)):
                    if docClass not in unigramDocClasses:
                        unigramDocClasses[docClass] = {}
                        bigramDocClasses[docClass] = {}
                    unigramKey = words[i]
                    if i == 0:
                        bigramKey = 'SS ' + words[i]
                    else:
                        bigramKey = words[i - 1] + ' ' + words[i]
                    if unigramKey in unigramDocClasses[docClass]:
                        unigramDocClasses[docClass][unigramKey] += 1
                    else:
                        unigramDocClasses[docClass][unigramKey] = 1
                    if bigramKey in bigramDocClasses[docClass]:
                        bigramDocClasses[docClass][bigramKey] += 1
                    else:
                        bigramDocClasses[docClass][bigramKey] = 1
        probabilities = {}
        for docClass in unigramDocClasses:
            unigramProbability = {}
            bigramProbability = {}
            probabilities[docClass] = {}
            for word in unigramDocClasses[docClass]:
                unigramProbability[word] = unigramDocClasses[docClass][word] / len(unigramDocClasses[docClass])
            for biwords in bigramDocClasses[docClass]:
                [first, second] = biwords.split()
                bigramProbability[biwords] = bigramDocClasses[docClass][biwords] / unigramDocClasses[docClass][first]
            for biwords in bigramDocClasses[docClass]:
                [first, second] = biwords.split()
                probabilities[docClass][biwords] = math.log2(unigramProbability[first]*self.unigramFactor) + math.log2(bigramProbability[biwords]*self.bigramFactor)
        classProbability = {}
        for docClass in docClassOccuringCounts:
            classProbability[docClass] = docClassOccuringCounts[docClass] / allCount
        return probabilities, classProbability

    # def calculateBigramModel(self):
    #     unigramModel = self.calculateUnigramModel()
    #     uniCounts = unigramModel[0]
    #     classProbability = unigramModel[1]
    #     uniProbabilities = unigramModel[2]
    #     docClasses = {}
    #     with open(self.trainFile, 'r') as f:
    #         for line in f:
    #             pivot = line.find('@')
    #             docClass = line[0:pivot]
    #             words = line[pivot + 10:].split()
    #             for i in range(len(words)):
    #                 if docClass not in docClasses:
    #                     docClasses[docClass] = {}
    #                 if i == 0:
    #                     key = 'SS ' + words[i]
    #                 else:
    #                     key = words[i - 1] + ' ' + words[i]
    #                 if key in docClasses[docClass]:
    #                     docClasses[docClass][key] += 1
    #                 else:
    #                     docClasses[docClass][key] = 1
    #     probabilities = {}
    #     for docClass in docClasses:
    #         docClassProbability = {}
    #         for biwords in docClasses[docClass]:
    #             [first, second] = biwords.split()
    #             docClassProbability[biwords] = docClasses[docClass][biwords] / uniCounts[docClass][first]
    #         probabilities[docClass] = docClassProbability
    #     return probabilities, classProbability, uniProbabilities
