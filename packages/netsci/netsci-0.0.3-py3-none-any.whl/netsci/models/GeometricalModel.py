import logging

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

from netsci.spatial.coords import core_connectivity_features, enrich_connections


feature_sets = {
    'dd' : ['offset_rho'],
    'ddz': ['offset_rho', 'sign_dz'],
    'od' : ['offset_rho', 'sign_dz', 'offset_az', 'offset_el'],
    'pd' : ['offset_rho', 'sign_dz', 'offset_az', 'offset_el', 'from_rho', 'from_az', 'from_el']
}


class GeometricalModel:
    default_classifier_kws = {
        'learning_rate': 0.01,
        'n_estimators': 500, 
        'max_depth': 5,
        'random_state': 1234,
    }
    # default_classifier_kws = { 'n_estimators': 20, 'max_depth': 3, 'random_state': 1234, 'verbose': 1}  # For debugging
    
    
    def __init__(self, type, classifier=None, classifier_kws={}):
        self.type = type
        self.classifier_kws = {**self.default_classifier_kws, **classifier_kws}
        
        self.feature_names = feature_sets[type]
        
        logging.info(f'classifier_kws: {self.classifier_kws}')
        logging.info(f'feature_names: {self.feature_names}')
        
    
    def fit(self, positions, A):
        data = self._preprocess(positions, A)
        X, y = data[self.feature_names], data['connection']

        self.clf = GradientBoostingClassifier(**self.classifier_kws)
        self.clf.fit(X, y)
    
    
    def predict(self, positions):
        raise NotImplementedError
    
    
    def predict_proba(self, positions):
        data = self._preprocess(positions)
        X = data[self.feature_names]
        
        datap = data.assign(p=self.clf.predict_proba(X)[:,1])
        P = datap.pivot_table(index='from', columns='to', values=['p']).fillna(0).values
        return P

    
    @staticmethod
    def _preprocess(positions, A=None):
        assert (~np.isnan(positions)).all(), 'Positions can not contain NaN values!'

        core_features = core_connectivity_features(positions, A)
        features = enrich_connections(core_features)
        
        # display(features.head())
        # display(features[['connection', 'contacts']].sum().to_frame('total'))
        return features


class BaseValidationError(ValueError):
    pass
