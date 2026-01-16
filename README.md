# The Empathy Engine  
### Emotion-Aware Text-to-Speech with Intensity Scaling

---

## 1. Problem Statement

Modern AI systems can generate accurate text responses, but their **voice output often lacks emotional depth**. Traditional Text-to-Speech (TTS) systems sound monotonic and robotic, failing to convey enthusiasm, concern, frustration, or empathy — qualities that are critical in sales, customer support, and human–AI interaction.

The challenge was to build an **Empathy Engine**:  
a system that dynamically **modulates speech characteristics** (pitch, speed, volume) based on the **emotion and emotional intensity** present in the input text.

---

## 2. Solution Overview

The Empathy Engine introduces an **emotion-aware layer** between text understanding and speech synthesis.

Instead of directly converting text to speech, the system:
1. Detects the **emotion** expressed in the text
2. Measures the **intensity** of that emotion
3. Maps emotion + intensity to **vocal parameters**
4. Generates **emotionally expressive speech**

This results in speech that:
- sounds excited for positive messages,
- slower and subdued for sadness,
- controlled but firm for frustration,
- calm and reassuring for concern.

---

## 3. System Architecture
Input Text
↓
Emotion Detection (Transformer Model)
↓
Emotion Normalization + Intensity Scaling
↓
Emotion → Voice Parameter Mapping
↓
Edge TTS Speech Synthesis
↓
Audio Output (.mp3)


---

## 4. Emotion Detection

We use a pretrained transformer-based emotion classifier: j-hartmann/emotion-english-distilroberta-base


This model outputs probabilities across multiple emotions.  
The emotion with the highest probability is selected, and that probability is treated as the **emotion intensity** (range 0–1).

### Emotion Normalization

| Model Emotion | Engine Emotion |
|---------------|----------------|
| joy           | happy          |
| surprise      | excited        |
| anger         | frustrated     |
| sadness       | sad            |
| fear          | concerned      |
| neutral       | neutral        |

This abstraction keeps the system **clean, explainable, and extensible**.

---

## 5. Intensity Scaling (Key Innovation)

Instead of binary emotion switching, the Empathy Engine uses **continuous intensity scaling**.

- Emotion determines *how* the voice should change
- Confidence score determines *how much* it should change

Mathematically: scaled_value = base_emotion_value × intensity

This produces smoother, more human-like speech variation.

---

## 6. Emotion → Voice Mapping

Maximum modulation values at full intensity (confidence ≈ 1.0):

| Emotion    | Rate | Pitch (Hz) | Volume |
|------------|------|------------|--------|
| happy      | +15% | +40Hz      | +5%    |
| excited    | +25% | +70Hz      | +8%    |
| frustrated | −10% | −50Hz      | +6%    |
| sad        | −20% | −60Hz      | −5%    |
| concerned  | −5%  | −30Hz      | +3%    |
| neutral    | 0%   | 0Hz        | 0%     |

These values are scaled proportionally using the detected intensity.

---

## 7. Text-to-Speech Engine

- **Engine**: Microsoft Edge TTS (Python `edge-tts`)
- **Default Voice**: `en-US-GuyNeural` (male)
- **Why Edge TTS?**
  - Free (no API keys or billing)
  - High-quality neural voices
  - Supports pitch (Hz), rate (%), and volume (%)

---

## 8. Tech Stack

- **Language**: Python 3.9+
- **Emotion Analysis**: Hugging Face Transformers
- **Model**: DistilRoBERTa (emotion classification)
- **Text-to-Speech**: Edge TTS (Microsoft)
- **Audio Output**: MP3
- **Interface**: Command Line Interface (CLI)

---


## 9. Project Structure

empathy-engine/
├── src/
│ └── empathy_engine/
│ ├── emotion.py          # Emotion detection
│ ├── mapping.py          # Intensity scaling & voice mapping
│ ├── tts.py              # Edge TTS synthesis
│ └── cli.py              # CLI interface
├── outputs/              # Generated audio files
├── requirements.txt
├── pyproject.toml
└── README.md

## 10. Setup Instructions

### a) Create Virtual Environment

'''bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
'''

### b) Install Dependencies
pip install -r requirements.txt
pip install -e .

▶️ How to Run the Empathy Engine
From the project root:
    python -m empathy_engine.cli "I am really frustrated with this delay."
    python -m empathy_engine.cli "This is the best news I've heard all day!"






