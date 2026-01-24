from repository.model_repository import Model_Repository
import joblib
class Model_Service:

    def __init__(self, repository: Model_Repository):
        self.repository = repository

    def predict (self):
        ...
    def create (self):
        ...