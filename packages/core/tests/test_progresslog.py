import pytest

from Final2x_core.util.progressLog import PrintProgressLog


class Test_ProgressLog:
    def test_set(self) -> None:
        p = PrintProgressLog()
        p.set(10, 2)
        assert p.Total == 20
        assert p.progressCurrent == 0
        assert p.sr_n == 2

        p.progressCurrent = 7
        p.set(3, 1)
        assert p.Total == 3
        assert p.progressCurrent == 0
        assert p.sr_n == 1

        with pytest.raises(AssertionError):
            p.set(0, 2)
        with pytest.raises(AssertionError):
            p.set(10, 0)
        with pytest.raises(AssertionError):
            p.set(10, -1)
        with pytest.raises(AssertionError):
            p.set(-1, 2)
