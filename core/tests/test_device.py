import torch

from Final2x_core.util.device import get_device


def test_get_device_preserves_index() -> None:
    assert get_device("cuda:1") == torch.device("cuda:1")
    assert get_device("cpu:0") == torch.device("cpu:0")
