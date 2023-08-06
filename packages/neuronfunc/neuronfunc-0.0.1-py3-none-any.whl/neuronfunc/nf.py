class nf():
    def __init__(self, inputs, weight, bias):
        return (inputs * weight) + bias

class nfr():
    def __init__(self, inputs, weight, bias):
        return (weight * inputs) + bias
