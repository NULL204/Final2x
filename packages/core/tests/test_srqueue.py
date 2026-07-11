import importlib
from pathlib import Path

import numpy as np
from pytest import MonkeyPatch

from Final2x_core import SRConfig, sr_queue
from Final2x_core.util import PrintProgressLog

from .util import CONFIG_PATH


class Test_SRQUEUE:
    def test_queue(self) -> None:
        config: SRConfig = SRConfig.from_yaml(CONFIG_PATH)
        config.target_scale = 1.14514
        sr_queue(config=config)

    def test_invalid_image_reports_decode_failure(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
        invalid_image = tmp_path / "invalid.png"
        invalid_image.write_bytes(b"not an image")
        errors: list[str] = []

        class StubLogger:
            def info(self, _message: str) -> None:
                pass

            def warning(self, _message: str) -> None:
                pass

            def error(self, message: str) -> None:
                errors.append(message)

            def success(self, _message: str) -> None:
                pass

        class StubSRWrapper:
            def __init__(self, config: SRConfig) -> None:
                PrintProgressLog().set(len(config.input_path), 1)

            def process(self, _img: np.ndarray) -> None:
                raise AssertionError("invalid images must be skipped")

        srqueue_module = importlib.import_module("Final2x_core.SRqueue")
        monkeypatch.setattr(srqueue_module, "logger", StubLogger())
        monkeypatch.setattr(srqueue_module, "SRWrapper", StubSRWrapper)

        config = SRConfig(
            pretrained_model_name="test-model",
            device="cpu",
            output_path=tmp_path,
            input_path=[invalid_image],
        )
        srqueue_module.sr_queue(config)

        assert errors == ["Failed to decode image."]
        assert list((tmp_path / "outputs").iterdir()) == []
