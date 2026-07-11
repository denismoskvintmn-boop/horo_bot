from app.astronomy.planets import get_planet_positions, get_zodiac_sign


def test_get_zodiac_sign():
    assert get_zodiac_sign(0) == "Aries"
    assert get_zodiac_sign(30) == "Taurus"
    assert get_zodiac_sign(60) == "Gemini"
    assert get_zodiac_sign(90) == "Cancer"
    assert get_zodiac_sign(120) == "Leo"
    assert get_zodiac_sign(330) == "Pisces"


def test_get_planet_positions():
    import swisseph as swe

    jd = swe.julday(2025, 1, 1, 12.0)
    positions = get_planet_positions(jd)
    assert isinstance(positions, dict)
    assert "Sun" in positions
    assert "Moon" in positions
    assert "sign" in positions["Sun"]
