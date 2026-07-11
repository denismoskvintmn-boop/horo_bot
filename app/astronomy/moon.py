from datetime import date, datetime, timezone


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


def get_moon_phase(target_date: date) -> dict:
    """Calculate moon phase for a given date using a simplified algorithm."""
    jd = _julian_day(target_date)

    # Known new moon: January 6, 2000 18:14 UTC
    known_new_moon_jd = 2451550.1
    synodic_month = 29.53058867

    days_since_known = jd - known_new_moon_jd
    cycles = days_since_known / synodic_month
    phase = (cycles % 1.0) * synodic_month

    # Phase angle in degrees (0-360)
    phase_angle = (phase / synodic_month) * 360

    # Determine phase name
    if phase_angle < 22.5:
        phase_name = "New Moon"
    elif phase_angle < 67.5:
        phase_name = "Waxing Crescent"
    elif phase_angle < 112.5:
        phase_name = "First Quarter"
    elif phase_angle < 157.5:
        phase_name = "Waxing Gibbous"
    elif phase_angle < 202.5:
        phase_name = "Full Moon"
    elif phase_angle < 247.5:
        phase_name = "Waning Gibbous"
    elif phase_angle < 292.5:
        phase_name = "Last Quarter"
    elif phase_angle < 337.5:
        phase_name = "Waning Crescent"
    else:
        phase_name = "New Moon"

    # Illumination percentage
    illumination = (1 - (phase_angle / 360)) * 100
    if phase_angle > 180:
        illumination = ((phase_angle - 180) / 180) * 100

    # Simplified moon longitude approximation
    moon_longitude = (phase_angle + 180) % 360

    return {
        "phase_angle": round(phase_angle, 2),
        "phase_name": phase_name,
        "illumination_percent": round(illumination, 1),
        "moon_longitude": round(moon_longitude, 4),
    }
