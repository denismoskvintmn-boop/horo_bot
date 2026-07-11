from app.ai.prompts import SYSTEM_PROMPT, build_user_prompt


def test_system_prompt_exists():
    assert len(SYSTEM_PROMPT) > 0
    assert "астролог" in SYSTEM_PROMPT.lower()


def test_build_user_prompt():
    user_data = {
        "name": "Test",
        "gender": "male",
        "birth_date": "2000-01-01",
        "birth_city": "Moscow",
    }
    astronomy_data = {
        "date": "2025-01-01",
        "planets": {"Sun": {"sign": "Capricorn", "longitude": 280.5}},
        "moon": {"phase_name": "Full Moon", "illumination_percent": 99.0},
        "aspects": [{"planet1": "Sun", "planet2": "Moon", "aspect": "Conjunction"}],
    }

    prompt = build_user_prompt(user_data, astronomy_data)
    assert "Test" in prompt
    assert "Moscow" in prompt
    assert "Capricorn" in prompt
    assert "Full Moon" in prompt
