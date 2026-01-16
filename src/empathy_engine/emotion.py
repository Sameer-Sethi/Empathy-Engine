from transformers import pipeline

# Loaded Emotion Classifier
_emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

# Mapping Emotion of huggingFace to Engine
HF_TO_ENGINE_EMOTION = {
    "joy": "happy",
    "surprise": "excited",
    "anger": "frustrated",
    "sadness": "sad",
    "fear": "concerned",
    "neutral": "neutral"
}

def detect_emotion(text: str):
    """
    Analyze text and return emotion with intensity.

    Returns:
        engine_emotion (str): normalized emotion label
        confidence (float): intensity score (0-1)
        raw_scores (dict): full emotion probability distribution
    """
    if not text or not text.strip():
        return "neutral", 0.0, {}

    results = _emotion_classifier(text)[0]

    # Convert to {label: score}
    scores = {item["label"]: item["score"] for item in results}

    # Find strongest emotion
    top_emotion = max(scores, key=scores.get)
    confidence = scores[top_emotion]

    engine_emotion = HF_TO_ENGINE_EMOTION.get(top_emotion, "neutral")

    return engine_emotion, confidence, scores
