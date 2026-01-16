import argparse
import sys

from empathy_engine.emotion import detect_emotion
from empathy_engine.mapping import map_emotion_to_voice
from empathy_engine.tts import synthesize_speech


def main():
    parser = argparse.ArgumentParser(
        description="The Empathy Engine: Emotion-aware Text-to-Speech"
    )

    parser.add_argument(
        "text",
        type=str,
        help="Input text to synthesize with emotional modulation"
    )

    parser.add_argument(
        "--outdir",
        type=str,
        default="outputs",
        help="Directory to save generated audio (default: outputs)"
    )

    args = parser.parse_args()

    text = args.text.strip()
    if not text:
        print("❌ Error: Input text is empty.")
        sys.exit(1)

    # Detect emotion
    emotion, confidence, raw_scores = detect_emotion(text)

    # map them to voice
    voice_params = map_emotion_to_voice(emotion, confidence)

    # TTS synthesis
    output_path = synthesize_speech(
        text=text,
        voice_params=voice_params,
        output_dir=args.outdir
    )

    # Human-readable output
    print("\n=== Empathy Engine Output ===")
    print(f"Text       : {text}")
    print(f"Emotion    : {emotion}")
    print(f"Intensity  : {round(confidence, 3)}")
    print(f"Voice Params:")
    for k, v in voice_params.items():
        print(f"  - {k}: {v}")
    print(f"\nAudio saved to: {output_path}\n")


if __name__ == "__main__":
    main()
