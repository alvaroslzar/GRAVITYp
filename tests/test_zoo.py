import numpy as np
import pytest

from gravityp import Schwarzschild


def test_schwarzschild_photon_sphere():
    assert Schwarzschild().r_phs == (3.,)


def test_schwarzschild_radial_vanishes_at_horizon():
    schw = Schwarzschild()
    assert schw.radial(schw.inner_edge) == pytest.approx(0, abs=1e-12)
