"""
math_tool.py
Handles all numeric weather unit conversions and calculations.
No LLM inference — pure deterministic math.
"""

from typing import Any, Dict, Optional


TOOL_SCHEMA = {
    "name": "math_tool",
    "description": (
        "Performs weather-related unit conversions and numeric calculations. "
        "Use for: Celsius↔Fahrenheit↔Kelvin, mph↔km/h, hPa↔inHg, heat index, "
        "dew point, wind chill. Do NOT use for comfort assessment or forecasts."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": [
                    "c_to_f", "f_to_c", "c_to_k", "k_to_c",
                    "mph_to_kmh", "kmh_to_mph",
                    "hpa_to_inhg", "inhg_to_hpa",
                    "mm_to_inches", "inches_to_mm",
                    "heat_index", "wind_chill", "dew_point"
                ],
                "description": "The conversion or calculation to perform"
            },
            "value": {
                "type": "number",
                "description": "Primary input value"
            },
            "secondary_value": {
                "type": "number",
                "description": (
                    "Secondary value for two-input calculations: "
                    "humidity % for heat_index and dew_point, "
                    "wind speed km/h for wind_chill"
                )
            }
        },
        "required": ["operation", "value"]
    }
}


def run(operation: str, value: float, secondary_value: Optional[float] = None) -> Dict[str, Any]:
    """Execute the requested weather math operation."""

    ops = {
        "c_to_f":       _c_to_f,
        "f_to_c":       _f_to_c,
        "c_to_k":       _c_to_k,
        "k_to_c":       _k_to_c,
        "mph_to_kmh":   _mph_to_kmh,
        "kmh_to_mph":   _kmh_to_mph,
        "hpa_to_inhg":  _hpa_to_inhg,
        "inhg_to_hpa":  _inhg_to_hpa,
        "mm_to_inches":     _mm_to_inches,
        "inches_to_mm":     _inches_to_mm,
        "heat_index":   _heat_index,
        "wind_chill":   _wind_chill,
        "dew_point":    _dew_point,
    }

    if operation not in ops:
        return {"error": f"Unknown operation: {operation}"}

    two_input_ops = {"heat_index", "wind_chill", "dew_point"}
    if operation in two_input_ops and secondary_value is None:
        return {
            "error": f"'{operation}' requires a secondary_value. "
                     f"Provide humidity % (heat_index/dew_point) or wind speed km/h (wind_chill)."
        }

    try:
        result = ops[operation](value, secondary_value)
        return result
    except Exception as e:
        return {"error": str(e)}


# ── Conversion implementations ──────────────────────────────────────────────

def _c_to_f(c, _=None):
    f = (c * 9 / 5) + 32
    return {
        "input": f"{c}°C",
        "result": round(f, 2),
        "unit": "°F",
        "formula": "(C × 9/5) + 32"
    }

def _f_to_c(f, _=None):
    c = (f - 32) * 5 / 9
    return {
        "input": f"{f}°F",
        "result": round(c, 2),
        "unit": "°C",
        "formula": "(F − 32) × 5/9"
    }

def _c_to_k(c, _=None):
    return {
        "input": f"{c}°C",
        "result": round(c + 273.15, 2),
        "unit": "K",
        "formula": "C + 273.15"
    }

def _k_to_c(k, _=None):
    return {
        "input": f"{k}K",
        "result": round(k - 273.15, 2),
        "unit": "°C",
        "formula": "K − 273.15"
    }

def _mph_to_kmh(mph, _=None):
    return {
        "input": f"{mph} mph",
        "result": round(mph * 1.60934, 2),
        "unit": "km/h",
        "formula": "mph × 1.60934"
    }

def _kmh_to_mph(kmh, _=None):
    return {
        "input": f"{kmh} km/h",
        "result": round(kmh / 1.60934, 2),
        "unit": "mph",
        "formula": "km/h ÷ 1.60934"
    }

def _hpa_to_inhg(hpa, _=None):
    return {
        "input": f"{hpa} hPa",
        "result": round(hpa * 0.02953, 4),
        "unit": "inHg",
        "formula": "hPa × 0.02953"
    }

def _inhg_to_hpa(inhg, _=None):
    return {
        "input": f"{inhg} inHg",
        "result": round(inhg / 0.02953, 2),
        "unit": "hPa",
        "formula": "inHg ÷ 0.02953"
    }

def _mm_to_inches(mm, _=None):
    return {
        "input": f"{mm} mm",
        "result": round(mm / 25.4, 4),
        "unit": "inches",
        "formula": "mm ÷ 25.4"
    }

def _inches_to_mm(inches, _=None):
    return {
        "input": f"{inches} inches",
        "result": round(inches * 25.4, 2),
        "unit": "mm",
        "formula": "inches × 25.4"
    }

def _heat_index(temp_c: float, humidity: float):
    """
    Rothfusz Heat Index formula.
    Valid when temp > 27°C and humidity > 40%.
    """
    T, R = temp_c, humidity
    if T < 27:
        return {
            "note": "Heat index is only meaningful above 27°C.",
            "input_temp": f"{T}°C",
            "input_humidity": f"{R}%",
            "result": T,
            "unit": "°C (no adjustment)"
        }
    HI = (-8.78469
          + 1.61139411 * T
          + 2.338549   * R
          - 0.14611605 * T * R
          - 0.01230809 * T ** 2
          - 0.01642482 * R ** 2
          + 0.00221173 * T ** 2 * R
          + 0.00072546 * T * R ** 2
          - 0.00000358 * T ** 2 * R ** 2)
    return {
        "input_temp": f"{T}°C",
        "input_humidity": f"{R}%",
        "result": round(HI, 2),
        "unit": "°C (feels like)",
        "formula": "Rothfusz Heat Index"
    }

def _wind_chill(temp_c: float, wind_kmh: float):
    """
    Environment Canada / NWS wind chill formula.
    Valid when temp < 10°C and wind > 4.8 km/h.
    """
    T, V = temp_c, wind_kmh
    if T >= 10:
        return {
            "note": "Wind chill only meaningful below 10°C.",
            "input_temp": f"{T}°C",
            "input_wind": f"{V} km/h",
            "result": T,
            "unit": "°C (no adjustment)"
        }
    WC = (13.12
          + 0.6215 * T
          - 11.37 * V ** 0.16
          + 0.3965 * T * V ** 0.16)
    return {
        "input_temp": f"{T}°C",
        "input_wind": f"{V} km/h",
        "result": round(WC, 2),
        "unit": "°C (feels like)",
        "formula": "Environment Canada Wind Chill"
    }

def _dew_point(temp_c: float, humidity: float):
    """Magnus formula approximation."""
    import math
    T, RH = temp_c, humidity
    a, b = 17.27, 237.7
    alpha = ((a * T) / (b + T)) + math.log(RH / 100.0)
    dp = (b * alpha) / (a - alpha)
    return {
        "input_temp": f"{T}°C",
        "input_humidity": f"{RH}%",
        "result": round(dp, 2),
        "unit": "°C (dew point)",
        "formula": "Magnus approximation"
    }
