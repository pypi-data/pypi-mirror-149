import os
import re
import json
import time
from typing import Optional, Union, List, Dict

import numpy as np

import ROOT

from quickstats import semistaticmethod
from quickstats.components import AbstractObject, ExtendedModel
from quickstats.utils.io import Verbosity
from quickstats.utils.root_utils import load_macro, get_macro_dir
from quickstats.maths.numerics import is_float, pretty_value

from quickstats.utils.general_enum import GeneralEnum


class WSComparer(AbstractObject):
    def __init__(self, ws_path_1:str, ws_path_2:str):
        self.set_targets(ws_path_1, ws_path_2)
        
    def set_targets(self, ws_path_1:str, ws_path_2:str):
        self.model_1 = ExtendedModel(ws_path_1, data_name=None, verbosity="WARNING")
        self.model_2 = ExtendedModel(ws_path_2, data_name=None, verbosity="WARNING")
        
        
    def test(self):
        "Category"
        "Obervables"
        "Datasets"
        "Snapshots"
        "NuisanceParameters"
        "GlobalObservables"
        "POIs"
        "AUXILIARY"
        "FUNCTIONS"