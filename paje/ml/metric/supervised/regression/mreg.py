from sklearn.metrics import r2_score,mean_squared_error

class Metrics:
    @classmethod
    def error(cls, data):
        return mean_squared_error(data.y,data.z)

    @classmethod
    def accuracy(cls, data):
        return r2_score(data.y, data.z)
