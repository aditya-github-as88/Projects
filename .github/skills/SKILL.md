# Weather Agent Skills

## SKILL: temperature_bands
Comfort bands (Celsius):
  < 0°C   → Freezing. Frostbite risk in wind.
  0–10°C  → Cold. Heavy clothing needed.
  10–20°C → Cool to mild.
  20–28°C → Comfortable. Ideal for activity.
  28–35°C → Warm to hot. Stay hydrated.
  35–40°C → Very hot. Limit outdoor activity.
  > 40°C  → Dangerous. Heat stroke risk.

## SKILL: unit_formulas
  Celsius → Fahrenheit : (C × 9/5) + 32
  Fahrenheit → Celsius : (F − 32) × 5/9
  Celsius → Kelvin     : C + 273.15
  mph → km/h           : × 1.60934
  hPa → inHg           : × 0.02953

## SKILL: direct_response_format
When the LLM answers without a tool, end with:

  Reasoning trace:
  - Knowledge used: [category]
  - Confident: [facts]
  - Uncertain: [gaps]
  - New tool suggested: [yes/no and why]
