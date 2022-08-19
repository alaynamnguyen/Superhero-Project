from sklearn.base import BaseEstimator, TransformerMixin

# Filter dataframe for top closest to user inputted data
def closest(data, gender, eye_color, race, hair_color, height, publisher, skin_color, weight, top=3):
    filtered = data.loc[(data["gender"] == gender)
            & (data["eye color"] == eye_color)
            & (data["race"] == race)
            & (data["hair color"] == hair_color)
            & (data["publisher"] == publisher)
            & (data["skin color"] == skin_color)]
    if len(filtered) < top:
        filtered = data.loc[(data["gender"] == gender)
            & (data["eye color"] == eye_color)
            & (data["race"] == race)
            & (data["hair color"] == hair_color)
            & (data["publisher"] == publisher)]
        if len(filtered) < top:
            filtered = data.loc[(data["gender"] == gender)
            & (data["eye color"] == eye_color)
            & (data["race"] == race)
            & (data["hair color"] == hair_color)]
            if len(filtered) < top:
                filtered = data.loc[(data["gender"] == gender)
                & (data["eye color"] == eye_color)
                & (data["race"] == race)]
                if len(filtered) < top:
                    filtered = data.loc[(data["gender"] == gender)
                    & (data["eye color"] == eye_color)]
                    if len(filtered) < top:
                        filtered = data.loc[(data["gender"] == gender)]
    return filtered

class CustomRemover(BaseEstimator, TransformerMixin):

    def __init__(self, useless_attribs):
        self.useless_attribs = useless_attribs

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        X_copy = X_copy.drop(self.useless_attribs, axis=1)

        return X_copy