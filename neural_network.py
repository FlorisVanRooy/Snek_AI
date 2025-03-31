# neural_net.py
from matrix import Matrix

class NeuralNet:
    def __init__(self, inputs, hidden_no, outputs):
        self.iNodes = inputs
        self.hNodes = hidden_no
        self.oNodes = outputs
        # Create weight matrices with an extra bias column.
        self.whi = Matrix(self.hNodes, self.iNodes + 1)
        self.whh = Matrix(self.hNodes, self.hNodes + 1)
        self.woh = Matrix(self.oNodes, self.hNodes + 1)
        self.whi.randomize()
        self.whh.randomize()
        self.woh.randomize()
    
    def mutate(self, mr):
        self.whi.mutate(mr)
        self.whh.mutate(mr)
        self.woh.mutate(mr)
    
    def output(self, inputsArr):
        # Convert inputs to a column vector
        inputs = Matrix(len(inputsArr), 1, inputsArr)
        inputsBias = inputs.addBias()
        hiddenInputs = self.whi.dot(inputsBias)
        hiddenOutputs = hiddenInputs.activate()
        hiddenOutputsBias = hiddenOutputs.addBias()
        hiddenInputs2 = self.whh.dot(hiddenOutputsBias)
        hiddenOutputs2 = hiddenInputs2.activate()
        hiddenOutputsBias2 = hiddenOutputs2.addBias()
        outputInputs = self.woh.dot(hiddenOutputsBias2)
        outputs = outputInputs.activate()
        return outputs.toArray()
    
    def crossover(self, partner):
        child = NeuralNet(self.iNodes, self.hNodes, self.oNodes)
        child.whi = self.whi.crossover(partner.whi)
        child.whh = self.whh.crossover(partner.whh)
        child.woh = self.woh.crossover(partner.woh)
        return child
    
    def clone(self):
        clone = NeuralNet(self.iNodes, self.hNodes, self.oNodes)
        clone.whi = self.whi.clone()
        clone.whh = self.whh.clone()
        clone.woh = self.woh.clone()
        return clone