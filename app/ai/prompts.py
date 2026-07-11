SYSTEM_PROMPT = """Ты — опытный астролог-эксперт, который составляет персональные ежедневные гороскопы.

Твой стиль:
- Говоришь温暖 и дружелюбно, как старый друг-астролог
- Используешь конкретные астрономические данные для прогнозов
- Даёшь практичные советы на день
- Упоминаешь влияние планет и аспектов
- Пишешь на русском языке
- Объём гороскопа — 300-500 слов

Формат ответа:
1. Приветствие с именем
2. Общий прогноз на день
3. Любовь и отношения
4. Работа и финансы
5. Здоровье и энергия
6. Совет дня
7. Счастливые числа и цвет

Используй переданные астрономические данные для формирования прогноза."""


def build_user_prompt(user_data: dict, astronomy_data: dict) -> str:
    planets_text = "\n".join(
        f"  {name}: {data['sign']} ({data['longitude']}°)"
        for name, data in astronomy_data.get("planets", {}).items()
    )

    aspects_text = "\n".join(
        f"  {a['planet1']} {a['aspect']} {a['planet2']}"
        for a in astronomy_data.get("aspects", [])
    )

    moon = astronomy_data.get("moon", {})

    return f"""Составь персональный гороскоп на {astronomy_data.get('date', 'сегодня')}.

Данные пользователя:
- Имя: {user_data['name']}
- Пол: {user_data['gender']}
- Дата рождения: {user_data['birth_date']}
- Место рождения: {user_data['birth_city']}
- Время рождения: {user_data.get('birth_time', 'неизвестно')}

Астрономические данные на сегодня:
Положение планет:
{planets_text}

Фаза Луны: {moon.get('phase_name', 'N/A')} (освещённость: {moon.get('illumination_percent', 0)}%)

Аспекты:
{aspects_text}

На основе этих данных составь детальный персональный гороскоп."""
