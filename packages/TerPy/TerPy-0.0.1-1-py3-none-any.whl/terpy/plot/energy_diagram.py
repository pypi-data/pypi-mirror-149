import matplotlib.pyplot as plt

__all__ = [
    'EnergyDiagram'
]


class EnergyDiagram:
    def __init__(self):
        self.levels = []
    def add_level(self, level):
        pass
    def plot(self):
        self.figure = plt.figure()


class EnergyLevel:
    def __init__(self, energies):
        self.energies = energies
    
    @classmethod
    def from_matter(cls, matter):
        return cls({model: matter.get_gibbs_energy(*model) for model in matter.get_models()})

