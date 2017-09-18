#from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib

class modelHandler:
    def __init__(self):
        pass
        #self.model = MLPRegressor()

    def setModel(self, model):
        self.model = model

    def getModel(self):
        return self.model

    def loadModel(self, tramline):
        self.model = joblib.load('models/MLPRegressor_' + tramline + '.pkl')

    def dumpModel(self, tramline):
        joblib.dump(self.model, 'models/MLPRegressor_' + tramline + '.pkl')
