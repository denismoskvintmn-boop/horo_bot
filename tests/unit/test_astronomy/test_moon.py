from app.astronomy.moon import get_moon_phase


def test_get_moon_phase_returns_dict():
    import swisseph as swe

    from app.core.config import settings

    swe.set_ephe_path(settings.SWISSEPH_PATH)
    jd = swe.julday(2025, 1, 1, 12.0)
    result = get_moon_phase(jd)
    assert isinstance(result, dict)
    assert "phase_name" in result
    assert "illumination_percent" in result
    assert "phase_angle" in result
