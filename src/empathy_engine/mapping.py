from typing import Dict

# I have take male voice as default
DEFAULT_VOICE = "en-US-GuyNeural"

# Hard coded the parameters for emotion. These are max modulation values
EMOTION_BASE_PARAMS = {
    "happy":       {"rate": 15,  "pitch": 10,  "volume": 5},
    "excited":     {"rate": 25,  "pitch": 18,  "volume": 8},
    "frustrated":  {"rate": -10, "pitch": -12, "volume": 6},
    "sad":         {"rate": -20, "pitch": -15, "volume": -5},
    "concerned":   {"rate": -5,  "pitch": -8,  "volume": 3},
    "neutral":     {"rate": 0,   "pitch": 0,   "volume": 0},
}

def _scale(value: float, intensity: float) -> int:
    """
    Linearly scale a modulation value by intensity (0-1).
    """
    return int(round(value * intensity))

def map_emotion_to_voice(
    emotion: str,
    confidence: float
) -> Dict[str, str]:
    """
    Maps emotion + confidence to Edge TTS voice parameters.

    Returns:
        {
            "voice": str,
            "rate": "+10%",
            "pitch": "-5%",
            "volume": "+3%"
        }
    """

    # Clamp confidence safely
    intensity = max(0.0, min(confidence, 1.0))

    base = EMOTION_BASE_PARAMS.get(emotion, EMOTION_BASE_PARAMS["neutral"])

    rate = _scale(base["rate"], intensity)
    pitch = _scale(base["pitch"], intensity)
    volume = _scale(base["volume"], intensity)

    def fmt(val: int) -> str:
        return f"{'+' if val >= 0 else ''}{val}%"

    return {
        "voice": DEFAULT_VOICE,
        "rate": fmt(rate),
        "pitch": fmt(pitch),
        "volume": fmt(volume),
    }
