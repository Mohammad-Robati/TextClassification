class TrainModel:

    def __init__(self, trainFile, unigramFactor, bigramFactor):
        self.trainFile = trainFile
        self.unigramFactor = unigramFactor
        self.bigramFactor = bigramFactor
        self.unigramDocClasses = {}
        self.bigramDocClasses = {}
        self.docClassOccuringCounts = {}
        self.allCount = 0

    def calculateCounts(self):
        unigramDocClasses = self.unigramDocClasses
        bigramDocClasses = self.bigramDocClasses
        docClassOccuringCounts = self.docClassOccuringCounts
        allCount = self.allCount
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
        self.unigramDocClasses = unigramDocClasses
        self.bigramDocClasses = bigramDocClasses
        self.docClassOccuringCounts = docClassOccuringCounts
        self.allCount = allCount

    def calculateModel(self):
        self.calculateCounts()
        return self.getProbability, self.getClassProbabilities()

    def getUnigramProbability(self, word, docClass):
        if word not in self.unigramDocClasses[docClass]:
            return 0
        return self.unigramDocClasses[docClass][word] / len(self.unigramDocClasses[docClass])

    def getBigramProbability(self, biwords, docClass):
        if biwords not in self.bigramDocClasses[docClass]:
            return 0
        [first, second] = biwords.split()
        return self.bigramDocClasses[docClass][biwords] / self.unigramDocClasses[docClass][first]

    def getProbability(self, biwords, docClass):
        [first, second] = biwords.split()
        return self.bigramFactor * self.getBigramProbability(biwords, docClass) + \
               self.unigramFactor * self.getUnigramProbability(second, docClass) + \
               (1 - self.unigramFactor - self.bigramFactor)

    def getClassProbabilities(self):
        classProbabilities = {}
        for docClass in self.docClassOccuringCounts:
            classProbabilities[docClass] = self.docClassOccuringCounts[docClass] / self.allCount
        return classProbabilities
