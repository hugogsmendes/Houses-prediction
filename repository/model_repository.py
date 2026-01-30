from models.predictions import Prediction

class Model_Repository:

    def __init__(self, session):
        self.session = session

    def create (self, prediction: dict) -> Prediction:

        new_prediction = Prediction(**prediction)
        self.session.add(new_prediction)
        self.session.commit()
        self.session.refresh(new_prediction)
        return new_prediction
    
    def high_price (self) -> Prediction:

        house_price_high = self.session.query(Prediction).order_by(Prediction.preco_previsto.desc()).first()

        return house_price_high