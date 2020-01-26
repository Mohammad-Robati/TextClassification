from train import TrainModel
from test import TestModel
from assess import Assessment

trainer = TrainModel('HAM-Train-Test/HAM-Train.txt', 0.1, 0.9)
tester = TestModel('HAM-Train-Test/HAM-Test.txt')
# trainer = TrainModel('HAM-Train-Test/mytrain.txt')
# tester = TestModel('HAM-Train-Test/mytest.txt')
assessor = Assessment()
assessor.calculateEstimationParameters(tester.testModel(trainer.calculateModel()))
