from const import *

class DataManager:
    def __init__(self, path):
        self.path = path
    
    def decode(self, word):
        sequence = []
        for letter in word:
            if (letter in LETTERS[1]):
                sequence.append(1)
            elif (letter in LETTERS[0]):
                sequence.append(0)
            else:
                continue
        
        if (len(sequence) != 4): return False
        if (tuple(sequence) in EXCEPTIONS): return False

        return tuple(sequence)

    def GetData(self):
        data = []

        with open(self.path, "r", encoding="utf-8") as file:
            for line in file.readlines():
                proc_result = self.decode(line.lower())
                if (proc_result != False): data.append(proc_result)
        
        print("Training data are processed.")

        return data

