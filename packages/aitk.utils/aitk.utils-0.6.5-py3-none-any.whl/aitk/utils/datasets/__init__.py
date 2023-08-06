# -*- coding: utf-8 -*-
# *************************************
# aitk.robots: Python robot simulator
#
# Copyright (c) 2020 Calysto Developers
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.robots
#
# *************************************

import os

_aitk_base_dir = os.path.expanduser("~")
if not os.access(_aitk_base_dir, os.W_OK):
    _aitk_base_dir = "/tmp"

_aitk_dir = os.path.join(_aitk_base_dir, ".aitk")

if not os.path.exists(_aitk_dir):
    try:
        os.makedirs(_aitk_dir)
    except OSError:
        pass


def get_dataset(dataset=None):
    """
    Download and return a dataset.

    Args:
        dataset (str): one of "digits6x6", "dogs-vs-cats",
            "dogs", "cats", "dogs-vs-cats-100"

    Examples:
    ```python
    >>> get_dataset()
    ["cats", "digits6x6", "dogs", "dogs-vs-cats", "dogs-vs-cats-100"]

    >>> dataset = get_dataset("dogs")
    ```
    """
    if dataset is None:
        return [
            "cats",
            "digits6x6",
            "dogs",
            "dogs-vs-cats",
            "dogs-vs-cats-100",
        ]
    get = None
    if dataset == "digits6x6":
        from .digits6x6 import get
    elif dataset == "dogs-vs-cats":
        from .dogs_vs_cats import get
    elif dataset == "dogs":
        from .dogs_vs_cats import get_dogs as get
    elif dataset == "cats":
        from .dogs_vs_cats import get_cats as get
    elif dataset == "dogs":
        from .dogs_vs_cats import get_dogs as get
    elif dataset == "dogs-vs-cats-100":
        from .dogs_vs_cats_100 import get_dogs_vs_cats_100 as get
    else:
        raise Exception("unknown dataset name")
    return get()
