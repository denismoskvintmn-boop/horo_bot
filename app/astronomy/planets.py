from datetime import date


def _julian_day(target_date: date) -> float:
    """Convert date to Julian day number."""
    year = target_date.year
    month = target_date.month
    day = target_date.day

    if month <= 2:
        year -= 1
        month += 12

    a = year // 100
    b = 2 - a + a // 4

    return (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + day
        + b
        - 1524.5
    )


ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def get_zodiac_sign(longitude: float) -> str:
    """Convert ecliptic longitude to zodiac sign."""
    index = int(longitude / 30) % 12
    return ZODIAC_SIGNS[index]


# Orbital periods in days
_ORBITAL_PERIODS = {
    "Mercury": 87.969,
    "Venus": 224.701,
    "Earth": 365.256,
    "Mars": 686.980,
    "Jupiter": 4332.59,
    "Saturn": 10759.22,
    "Uranus": 30688.5,
    "Neptune": 60182.0,
    "Pluto": 90560.0,
}

# Mean longitudes at J2000.0 (Jan 1, 2000 12:00 TT)
_MEAN_LONGITUDES = {
    "Sun": 280.46,
    "Moon": 218.32,
    "Mercury": 252.25,
    "Venus": 181.98,
    "Mars": 355.43,
    "Jupiter": 34.35,
    "Saturn": 50.08,
    "Uranus": 314.06,
    "Neptune": 304.88,
    "Pluto": 238.93,
}

# Mean daily motions (degrees per day)
_DAILY_MOTIONS = {
    "Sun": 0.9856,
    "Moon": 13.1764,
    "Mercury": 4.0923,
    "Venus": 1.6021,
    "Mars": 0.5240,
    "Jupiter": 0.0831,
    "Saturn": 0.0334,
    "Uranus": 0.0117,
    "Neptune": 0.0060,
    "Pluto": 0.0040,
}


def get_planet_positions(target_date: date) -> dict[str, dict]:
    """Calculate approximate positions of planets for a given date."""
    jd = _julian_day(target_date)
    days_since_j2000 = jd - 2451545.0  # J2000.0 = Jan 1, 2000 12:00

    positions = {}
    for name in _MEAN_LONGITUDES:
        mean_lon = _MEAN_LONGITUDES[name]
        daily_motion = _DAILY_MOTIONS[name]

        longitude = (mean_lon + daily_motion * days_since_j2000) % 360

        positions[name] = {
            "longitude": round(longitude, 4),
            "latitude": 0.0,
            "sign": get_zodiac_sign(longitude),
        }

    return positions
