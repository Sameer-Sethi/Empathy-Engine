from empathy_engine.emotion import detect_emotion
from empathy_engine.mapping import map_emotion_to_voice
from empathy_engine.tts import synthesize_speech

text = "This is the best news I've heard all day!"

emotion, confidence, scores = detect_emotion(text)
voice_params = map_emotion_to_voice(emotion, confidence)

print("Emotion:", emotion)
print("Confidence:", round(confidence, 3))
print("Voice Params:", voice_params)

out = synthesize_speech(text, voice_params)
print("Saved:", out)
