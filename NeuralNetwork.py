from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader

from const import *
from DataManager import DataManager

import random, datetime

class NeuralNetwork:
    def __init__(self, count_enterNeurons, dataset_path, count_trainIterations, toSave = False, toLoad = False, name_savedNetwork = ""):
        self.count_enterNeurons = count_enterNeurons
        self.dataset_path = dataset_path
        self.count_trainIterations = count_trainIterations

        self.toSave = toSave
        self.toLoad = toLoad
        self.name_savedNetwork = name_savedNetwork

        self.data = []

        if (self.toLoad): self.Load()
        else:
            self.net = buildNetwork(self.count_enterNeurons, 3, 1, bias=True)
            self.ds = SupervisedDataSet(self.count_enterNeurons, 1)
    
    def load_dataset(self):
        dataManager = DataManager(self.dataset_path)

        self.data = dataManager.GetData()

    def Train(self):
        self.load_dataset()

        for i in range(50):
            for exception in EXCEPTIONS:
                self.ds.addSample(exception, (0))

        for line in self.data:
            self.ds.addSample(line, (1))

        print("Training data are loaded to the network.")

        trainer = BackpropTrainer(self.net)
        trainer.setData(self.ds)

        print("Training... please stand by")

        trainer.trainEpochs(self.count_trainIterations)

        print("Neural network is trained!")

        if (self.toSave): self.Save()
    
    def Save(self):
        print("Saving network...")

        now = datetime.datetime.now()
        NetworkWriter.writeToFile(self.net, "saved_networks/network_" + str(now.day) + "_" + str(now.month) + "_" + str(now.year))

        print("Neural network saved.")
    
    def Load(self):
        print("Loading network...")

        self.net = NetworkReader.readFrom(self.name_savedNetwork)

        print("Neural network loaded.")

    def Run(self):
        isCorrect = 0
        toCheck = ""

        while isCorrect < 0.5:
            toCheck = str(random.randint(0, 1)) + str(random.randint(0, 1)) + str(random.randint(0, 1)) + str(random.randint(0, 1))
            isCorrect = self.net.activate(tuple(map(int, toCheck)))
            print(toCheck, isCorrect)

        word = ""

        for letter in toCheck:
            word += random.choice(LETTERS[int(letter)])

        print(word)

        return word

if __name__ == "__main__":
    neuralNetwork = NeuralNetwork(4, "data/words.txt", 1000, toLoad=True, name_savedNetwork="saved_networks/network_8_3_2020")

    while True:
        neuralNetwork.Run()
        input()