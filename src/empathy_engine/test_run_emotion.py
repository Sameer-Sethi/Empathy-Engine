from empathy_engine.emotion import detect_emotion

text = "This is the best news I've heard all day!"
emotion, confidence, scores = detect_emotion(text)

print("Emotion:", emotion)
print("Confidence:", round(confidence, 3))
print("Raw scores:", scores)
