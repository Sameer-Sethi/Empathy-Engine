from typing import Dict

DEFAULT_VOICE = "en-US-GuyNeural"

# Max modulation at intensity = 1.0
EMOTION_BASE_PARAMS = {
    "happy":       {"rate": 15,  "pitch": 40,  "volume": 5},
    "excited":     {"rate": 25,  "pitch": 70,  "volume": 8},
    "frustrated":  {"rate": -10, "pitch": -50, "volume": 6},
    "sad":         {"rate": -20, "pitch": -60, "volume": -5},
    "concerned":   {"rate": -5,  "pitch": -30, "volume": 3},
    "neutral":     {"rate": 0,   "pitch": 0,   "volume": 0},
}

def _scale(value: float, intensity: float) -> int:
    return int(round(value * intensity))

def map_emotion_to_voice(emotion: str, confidence: float) -> Dict[str, str]:
    intensity = max(0.0, min(confidence, 1.0))
    base = EMOTION_BASE_PARAMS.get(emotion, EMOTION_BASE_PARAMS["neutral"])

    rate = _scale(base["rate"], intensity)
    pitch_hz = _scale(base["pitch"], intensity)
    volume = _scale(base["volume"], intensity)

    def fmt_pct(val: int) -> str:
        return f"{'+' if val >= 0 else ''}{val}%"

    def fmt_hz(val: int) -> str:
        return f"{'+' if val >= 0 else ''}{val}Hz"

    return {
        "voice": DEFAULT_VOICE,
        "rate": fmt_pct(rate),
        "pitch": fmt_hz(pitch_hz),
        "volume": fmt_pct(volume),
    }
