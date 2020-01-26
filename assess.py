class Assessment:

    def calculateEstimationParameters(self, results):
        stats = {}
        precision = {}
        recall = {}
        fMeasure = {}
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
            fMeasure[stat] = 2 * precision[stat] * recall[stat] / (precision[stat] + recall[stat])
        print(precision)
        print(recall)
        print(fMeasure)
