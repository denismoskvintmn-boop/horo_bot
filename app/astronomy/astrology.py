from datetime import date

from app.astronomy.moon import get_moon_phase
from app.astronomy.planets import get_planet_positions
from app.core.exceptions import AstronomyCalculationError


def get_aspects(target_date: date) -> list[dict]:
    """Calculate major aspects between planets."""
    planet_positions = get_planet_positions(target_date)
    aspects = []

    aspect_types = [
        ("Conjunction", 0, 10),
        ("Sextile", 60, 8),
        ("Square", 90, 8),
        ("Trine", 120, 8),
        ("Opposition", 180, 10),
    ]

    planet_names = list(planet_positions.keys())
    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1, p2 = planet_names[i], planet_names[j]
            diff = abs(
                planet_positions[p1]["longitude"] - planet_positions[p2]["longitude"]
            )
            if diff > 180:
                diff = 360 - diff

            for name, angle, orb in aspect_types:
                if abs(diff - angle) <= orb:
                    aspects.append(
                        {
                            "planet1": p1,
                            "planet2": p2,
                            "aspect": name,
                            "exact_angle": round(diff, 2),
                        }
                    )
                    break

    return aspects


def get_astronomy_data(target_date: date) -> dict:
    """Get all astronomical data for a given date."""
    try:
        planet_positions = get_planet_positions(target_date)
        moon_data = get_moon_phase(target_date)
        aspects = get_aspects(target_date)

        return {
            "date": target_date.isoformat(),
            "planets": planet_positions,
            "moon": moon_data,
            "aspects": aspects,
        }
    except Exception as e:
        raise AstronomyCalculationError(
            f"Failed to calculate astronomy data for {target_date}: {e}"
        )
