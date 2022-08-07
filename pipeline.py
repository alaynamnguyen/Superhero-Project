import streamlit as st
import pandas as pd
import numpy as np
import math
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from PIL import Image

# Pipeline things
class CustomRemover(BaseEstimator, TransformerMixin):

    def __init__(self, useless_attribs):
        self.useless_attribs = useless_attribs

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        X_copy = X_copy.drop(self.useless_attribs, axis=1)

        return X_copy  
   
   
   from sklearn.impute import SimpleImputer

useless_attribs = ["name", "Unnamed: 0"]
num_attribs = ['Height', 'Weight']
cat_attribs = ["Gender", "Eye color", "Race", "Hair color", "Publisher", "Skin color"]

num_pipeline = Pipeline([
  ("std_scaler", StandardScaler())
])

col_pipeline = ColumnTransformer([ 
  ("num", num_pipeline, num_attribs), 
  ("cat", OneHotEncoder(), cat_attribs),  
])

full_pipeline = Pipeline([   
  ("remover", CustomRemover(useless_attribs)),  
  ("col_pipeline", col_pipeline)
])


#end of pipeline things
