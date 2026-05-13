"""
sentiment_tool.py
Assesses the human experience of weather conditions —
comfort level, safety, activity suitability.
No LLM inference — rule-based against SKILL.md bands.
"""

from typing import Any, Dict, List, Optional


TOOL_SCHEMA = {
    "name": "sentiment_tool",
    "description": (
        "Assesses how weather conditions *feel* to humans — comfort, safety, "
        "activity suitability, emotional tone. Use when the query is about "
        "experience, not numeric conversion. Examples: 'Is 38°C dangerous?', "
        "'How does 15°C feel?', 'Is it safe to jog today?'"
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "temperature_c": {
                "type": "number",
                "description": "Temperature in Celsius"
            },
            "humidity_pct": {
                "type": "number",
                "description": "Relative humidity 0–100 (optional, improves assessment)"
            },
            "wind_kmh": {
                "type": "number",
                "description": "Wind speed in km/h (optional)"
            },
            "activity": {
                "type": "string",
                "description": "Activity the user wants to assess, e.g. 'jogging', 'outdoor work'",
            },
            "vulnerable_group": {
                "type": "boolean",
                "description": "True if assessing for elderly, children, or health-compromised individuals"
            }
        },
        "required": ["temperature_c"]
    }
}


def run(
    temperature_c: float,
    humidity_pct: float = None,
    wind_kmh: float = None,
    activity: str = None,
    vulnerable_group: bool = False
) -> Dict[str, Any]:

    comfort = _comfort_label(temperature_c)
    safety  = _safety_level(temperature_c, vulnerable_group)
    advice  = _build_advice(temperature_c, humidity_pct, wind_kmh, activity, vulnerable_group)
    emoji   = _emoji(temperature_c)
    factors = _contributing_factors(temperature_c, humidity_pct, wind_kmh)

    result = {
        "temperature_input": f"{temperature_c}°C",
        "comfort_label": comfort,
        "safety_level": safety,
        "emoji": emoji,
        "advice": advice,
        "contributing_factors": factors,
    }

    if activity:
        result["activity_suitability"] = _activity_suitability(
            temperature_c, activity, vulnerable_group
        )

    if humidity_pct and temperature_c > 27 and humidity_pct > 40:
        result["feels_like_note"] = (
            "Humidity is significant — actual discomfort is higher than temperature alone suggests. "
            "Consider using math_tool with operation=heat_index for the exact feels-like value."
        )

    return result


# ── Assessment helpers ───────────────────────────────────────────────────────

def _comfort_label(t: float) -> str:
    if t < 0:    return "Freezing"
    if t < 10:   return "Cold"
    if t < 18:   return "Cool"
    if t < 24:   return "Pleasant"
    if t < 30:   return "Warm"
    if t < 35:   return "Hot"
    if t < 40:   return "Very hot"
    return "Dangerous heat"


def _safety_level(t: float, vulnerable: bool) -> str:
    threshold_shift = -5 if vulnerable else 0
    adjusted = t - threshold_shift

    if adjusted < 0:
        return "CAUTION — frostbite risk in wind"
    if adjusted < 35:
        return "SAFE — normal precautions apply"
    if adjusted < 40:
        return "WARNING — limit outdoor exposure; stay hydrated"
    return "DANGER — risk of heat stroke; avoid outdoor activity"


def _build_advice(t, humidity, wind, activity, vulnerable) -> List[str]:
    advice = []

    if t > 35:
        advice.append("Stay in shaded or air-conditioned areas.")
        advice.append("Drink at least 500 ml of water per hour of outdoor activity.")
    if t > 40:
        advice.append("Avoid all non-essential outdoor activity.")
    if t < 0:
        advice.append("Wear insulated, wind-resistant clothing.")
        advice.append("Limit exposed skin to prevent frostbite.")
    if humidity and humidity > 70 and t > 28:
        advice.append("High humidity amplifies heat stress — reduce activity intensity.")
    if wind and wind > 50:
        advice.append("Strong winds — secure loose objects and avoid elevated areas.")
    if vulnerable:
        advice.append("Extra caution advised for this group — consult a health professional for extended exposure.")
    if not advice:
        advice.append("Conditions are comfortable for most people.")

    return advice


def _activity_suitability(t: float, activity: str, vulnerable: bool) -> str:
    act = activity.lower()
    high_exertion = any(w in act for w in ["run", "jog", "hike", "cycle", "sport", "exercise", "work"])

    if high_exertion:
        if t > 35:
            return f"NOT recommended — {t}°C is too hot for {activity}. Risk of heat exhaustion."
        if t > 30:
            return f"POSSIBLE with precautions — hydrate heavily, go early morning or evening."
        if t < 0:
            return f"POSSIBLE with warm gear — warm up indoors first."
        return f"SUITABLE — {t}°C is within safe range for {activity}."
    else:
        if t > 40:
            return f"NOT recommended even for light activity outdoors."
        return f"Generally suitable for {activity} at {t}°C."


def _contributing_factors(t, humidity, wind) -> List[str]:
    factors = [f"Temperature: {t}°C"]
    if humidity is not None:
        factors.append(f"Humidity: {humidity}% ({'high — worsens heat' if humidity > 60 else 'moderate'})")
    if wind is not None:
        label = "cooling benefit" if t > 25 else "wind chill effect"
        factors.append(f"Wind: {wind} km/h ({label})")
    return factors


def _emoji(t: float) -> str:
    if t < 0:    return "🥶"
    if t < 10:   return "🧥"
    if t < 18:   return "🌤️"
    if t < 24:   return "😊"
    if t < 30:   return "☀️"
    if t < 35:   return "🥵"
    return "🔥"
