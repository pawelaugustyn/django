from sklearn.externals import joblib

class modelHandler:
    def __init__(self):
        pass

    def setModel(self, model):
        self.model = model

    def getModel(self):
        return self.model

    def loadModel(self, tramline):
        self.model = joblib.load('machine_learning/models/MLPRegressor_' + tramline + '.pkl')

    def dumpModel(self, tramline):
        joblib.dump(self.model, 'machine_learning/models/MLPRegressor_' + tramline + '.pkl')

    def loadScalerModel(self, tramline):
        self.model = joblib.load('machine_learning/models/Scaler_' + tramline + '.pkl')

    def dumpScalerModel(self, tramline):
        joblib.dump(self.model, 'machine_learning/models/Scaler_' + tramline + '.pkl')
