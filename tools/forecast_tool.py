"""
forecast_tool.py
Analyses precipitation probability, multi-day trends, and weather outlook.
In production this would call an internal weather API.
Here it uses rule-based logic as a stand-in.
"""

from typing import Any, Dict, List


TOOL_SCHEMA = {
    "name": "forecast_tool",
    "description": (
        "Provides precipitation probability assessments and multi-day weather "
        "trend analysis. Use when the user asks about rain, storms, forecasts, "
        "or upcoming weather patterns. NOT for unit conversions or comfort ratings."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "precipitation_pct": {
                "type": "number",
                "description": "Probability of precipitation as a percentage 0–100"
            },
            "temperature_trend": {
                "type": "string",
                "enum": ["rising", "falling", "stable"],
                "description": "Direction of temperature change over the next 24–48 hours"
            },
            "humidity_pct": {
                "type": "number",
                "description": "Current relative humidity 0–100 (optional)"
            },
            "location_hint": {
                "type": "string",
                "description": "City or region name for contextual advice (optional)"
            }
        },
        "required": ["precipitation_pct"]
    }
}


def run(
    precipitation_pct: float,
    temperature_trend: str = "stable",
    humidity_pct: float = None,
    location_hint: str = None
) -> Dict[str, Any]:

    precip_label  = _precipitation_label(precipitation_pct)
    precip_advice = _precipitation_advice(precipitation_pct)
    trend_outlook = _trend_outlook(temperature_trend, humidity_pct)
    preparedness  = _preparedness_checklist(precipitation_pct, temperature_trend)

    return {
        "precipitation_probability": f"{precipitation_pct}%",
        "precipitation_label": precip_label,
        "precipitation_advice": precip_advice,
        "temperature_trend": temperature_trend,
        "trend_outlook": trend_outlook,
        "preparedness_checklist": preparedness,
        "location": location_hint or "Not specified",
        "data_source": "rule-based (replace with internal weather API in production)"
    }


# ── Forecast helpers ─────────────────────────────────────────────────────────

def _precipitation_label(pct: float) -> str:
    if pct <= 10:  return "Clear skies likely"
    if pct <= 30:  return "Slight chance of rain"
    if pct <= 60:  return "Rain possible"
    if pct <= 80:  return "Rain likely"
    return "Heavy rain expected"


def _precipitation_advice(pct: float) -> str:
    if pct <= 10:
        return "No rain gear needed. Enjoy clear conditions."
    if pct <= 30:
        return "Umbrella optional — light jacket recommended."
    if pct <= 60:
        return "Carry an umbrella. Rain may arrive at any time."
    if pct <= 80:
        return "Rain is probable. Waterproof clothing advised."
    return "Expect heavy rain. Avoid flood-prone areas. Stay updated on alerts."


def _trend_outlook(trend: str, humidity: float) -> str:
    if trend == "rising":
        if humidity and humidity > 70:
            return "Temperature rising with high humidity — increased discomfort expected. Watch for heat advisories."
        return "Temperature rising — warmer conditions ahead. Plan outdoor activity for cooler morning hours."
    if trend == "falling":
        return "Temperature falling — conditions will become more comfortable. Good window for outdoor activity."
    return "Temperature stable — consistent conditions expected for the next 24 hours."


def _preparedness_checklist(pct: float, trend: str) -> List[str]:
    checklist = []
    if pct > 40:
        checklist.append("✓ Carry waterproof jacket or umbrella")
        checklist.append("✓ Check local drainage / flood alerts if > 70%")
    if pct > 70:
        checklist.append("✓ Avoid low-lying or flood-prone routes")
        checklist.append("✓ Keep emergency contacts accessible")
    if trend == "rising":
        checklist.append("✓ Increase water intake over the next 24 hours")
    if trend == "falling":
        checklist.append("✓ Have a light jacket ready for evening")
    if not checklist:
        checklist.append("✓ No special preparation needed — standard conditions")
    return checklist
