import os
from importlib import import_module

import models
from models.base import CSCBaseModel


def get_models_classes():
    model_files = os.listdir(models.__path__[0])
    model_files.remove("base.py")
    model_files.remove("__init__.py")
    model_files.remove("model_test.py")

    for model in model_files:
        if not model.endswith(".py"):
            continue

        import_module("models." + model[:-3])

    models_classes = CSCBaseModel.__subclasses__()

    return models_classes


def get_model_names():
    models_classes = get_models_classes()
    return [model_class.model_name for model_class in models_classes]


def load_model(model_name: str, device='cpu', raise_error=True):
    models_classes = get_models_classes()
    for model_class in models_classes:
        if model_class.model_name == model_name:
            return model_class(device=device)

    if raise_error:
        raise NameError("找不到模型名称：" + model_name)

    return