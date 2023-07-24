from abc import ABC
from importlib import import_module


class CSCBaseModel(ABC):

    model_name = ""

    def __init__(self, *args, **kwargs):
        super(CSCBaseModel, self).__init__()

    def predict(self, sentence):
        """
        对sentence进行纠错。需要确保输入和输出的长度一致
        """
        pass
