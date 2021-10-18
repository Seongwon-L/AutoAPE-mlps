# -*- coding: utf-8 -*-
from typing import Dict

import torch
from mlps.core.apeflow.api.algorithms.AlgorithmAbstract import AlgorithmAbstract
from mlps.core.apeflow.api.algorithms.AlgorithmFactory import AlgorithmFactory
from mlps.core.apeflow.api.algorithms.pytorch import PyTorchAlgAbstract
from mlps.core.apeflow.interface.model.ModelAbstract import ModelAbstract


class PyTorchModel(ModelAbstract):
    model: PyTorchAlgAbstract

    def __init__(self, param_dict: Dict, ext_data=None):
        super().__init__(param_dict, ext_data)

        self.model = self._build()

    def _build(self) -> PyTorchAlgAbstract:
        model = AlgorithmFactory.create(
            param_dict=self.param_dict, ext_data=self.ext_data
        )
        model.load_model()

        return model

    def learn(self, dataset):
        self.model.learn(dataset)
        self.model.saved_model()
