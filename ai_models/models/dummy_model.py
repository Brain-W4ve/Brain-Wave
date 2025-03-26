from models.model import Model


class Dummy_Model(Model):
    def process(self, file_data):
        print("Will process nothing")