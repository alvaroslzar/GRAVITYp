import numpy as np
import pytest

from gravityp import Schwarzschild, SimpsonVisser


def test_schwarzschild_photon_sphere():
    assert Schwarzschild().r_phs == (3.,)


def test_schwarzschild_radial_vanishes_at_horizon():
    schw = Schwarzschild()
    assert schw.radial(schw.inner_edge) == pytest.approx(0, abs=1e-12)


# eps sets the precision of r_ph: errors larger than ~eps/2 are caught. As a
# approaches 3 the orbit becomes marginally unnstable (flat), so eps must grow
# for the potential difference to stay well above round-off (~1e-17)
@pytest.mark.parametrize("a, eps", [
    pytest.param(0.0, 1e-5, id="Schwarzschild"),
    pytest.param(1.0, 1e-5, id="black bounce"),
    pytest.param(2.0, 1e-5, id="extremal black bounce"),
    pytest.param(2.5, 1e-5, id="wormhole, photon sphere outside throat"),
    pytest.param(2.99, 1e-3, id="wormhole, flat maximum (a=2.99)"),
    pytest.param(2.999, 1e-3, id="wormhole, flat maximum (a=2.999)"),
    pytest.param(3.0, 1e-2, id="marginally unstable"),
    pytest.param(4.0, 1e-5, id="wormhole, photon sphere at throat"),
])
def test_sv_potential_maximum(a, eps):
    sv = SimpsonVisser(a)
    r_ph = sv.r_phs[0]
    # For a>=3, r_ph-eps<0, which is valid since V is symmetric
    assert sv.potential(r_ph) > sv.potential(r_ph-eps)
    assert sv.potential(r_ph) > sv.potential(r_ph+eps)


@pytest.mark.parametrize("a", [0, 1e-3, 1, 2-1e-3, 2])
def test_sv_radial_vanishes_at_horizon(a):
    sv = SimpsonVisser(a)
    assert sv.radial(sv.inner_edge) == pytest.approx(0, abs=1e-12)
