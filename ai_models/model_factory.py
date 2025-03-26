# from .models import *
# from .models.model import Model
from models import *
class Model_Factory:
    models = {
        "dummy": Dummy_Model()
    }

    def get_model(self, model_name: str) -> Model:
        return Model_Factory.models.get(model_name)

model_factory = Model_Factory()