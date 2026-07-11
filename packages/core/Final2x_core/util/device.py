from typing import Union

import torch
from cccv.util.device import DEFAULT_DEVICE


def get_device(device: str) -> Union[torch.device, str]:
    """
    Get device from string

    :param device: device string
    """
    device = device.lower()

    if device.startswith("auto"):
        return DEFAULT_DEVICE
    elif device.startswith("directml"):
        import torch_directml

        if ":" in device:
            try:
                return torch_directml.device(int(device.split(":", maxsplit=1)[1]))
            except (ValueError, IndexError):
                pass
        return torch_directml.device()
    elif any(device.startswith(prefix) for prefix in ("cpu", "cuda", "mps", "xpu")):
        return torch.device(device)
    else:
        return DEFAULT_DEVICE
