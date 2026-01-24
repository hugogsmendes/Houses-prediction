from repository.model_repository import Model_Repository
class Model_Service:

    def __init__(self, repository: Model_Repository):
        self.repository = repository