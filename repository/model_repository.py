from models.predictions import Prediction

class Model_Repository:

    def __init__(self, session):
        self.session = session

    def create (self, prediction: dict):

        new_prediction = Prediction(**prediction)
        self.session.add(new_prediction)
        self.session.commit()
        self.session.refresh(new_prediction)
        return new_prediction