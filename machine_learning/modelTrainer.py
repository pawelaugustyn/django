import sys
import warnings

import time

import numpy as np
import pandas as pd

from modelHandler import modelHandler

from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import RobustScaler

class modelTrainer:
    def __init__(self, tramline):
        self.tramline = tramline

    #read training dataset
    def readTrainingDataset(self):
        self.df = pd.read_csv('data/data_' + self.tramline + '.csv', header = 0, parse_dates = ['Time'])

    #separate training dataset features (Lat, Lon, Brigades) and targets (Time)
    def separateFeaturesAndTargets(self):
        self.features = self.df._get_numeric_data()
        self.features = self.features.drop('Lines', 1)
        self.targets = self.df['Time']

    #remove entries with spurious time stamps (more than 120 seconds early with respect to previous entry)
    def removeSpuriousTimestamps(self):
        indices = self.identifySpuriousTimestamps()
        self.removeEntries(indices)
        self.reindexDataset()

    def identifySpuriousTimestamps(self):
        drop_indices = []
        time_stamp = self.targets[0]
        diff_to_drop = -120
        for index, item in self.targets.iteritems():
            diff = np.timedelta64(item - time_stamp)/ np.timedelta64(1,'s')
            if diff < diff_to_drop:
                drop_indices.append(index)
            else:
                time_stamp = item
        return drop_indices

    def removeEntries(self, indices):
        self.features.drop(indices, inplace = True)
        self.targets.drop(indices, inplace = True)

    def reindexDataset(self):
        self.features.index = pd.RangeIndex(len(self.features.index))
        self.targets.index = pd.RangeIndex(len(self.targets.index))

    #scale training features with standard method
    def scaleFeatures(self):
        self.features = RobustScaler().fit_transform(self.features)

    #scale training targets (time) to number of seconds since midnight
    def scaleTargets(self):
        time_stamp = pd.Timestamp('2017-09-04')
        seconds_in_day = 86400
        self.targets = (self.targets - time_stamp) / np.timedelta64(1,'s')
        self.targets = self.targets % seconds_in_day

    #train model
    def trainModel(self):
        self.readTrainingDataset()
        self.separateFeaturesAndTargets()
        self.removeSpuriousTimestamps()
        self.scaleFeatures()
        self.scaleTargets()

        self.model = MLPRegressor(solver='lbfgs', hidden_layer_sizes=50,
                                  max_iter=150, shuffle=True, random_state=1,
                                  activation='relu')

        self.model.fit(self.features, self.targets)

        return self.model

    #get model score
    def getModelScore(self):
        return self.model.score(self.features, self.targets)


if __name__ == "__main__":
    np.seterr(all='warn')

    TRAMLINES = ['33', '22', '35', '24', '71', '27', '10', '18', '9', '7', '14', '15', '4', '23', '3', '25', '20', '26', '17', '1', '11', '2', '31', '13']

    for tramline in TRAMLINES:
        mt = modelTrainer(tramline)
        model = mt.trainModel()

        print 'tram line:', tramline, ', model score:', mt.getModelScore()

        mh = modelHandler()
        mh.setModel(model)
        mh.dumpModel(tramline)
