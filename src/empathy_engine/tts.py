import os
import asyncio
from datetime import datetime
from typing import Dict, Optional

import edge_tts


def _ensure_outputs_dir(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)


def _safe_filename(prefix: str = "empathy") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.mp3"


async def _synthesize_async(
    text: str,
    voice_params: Dict[str, str],
    output_path: str
) -> str:
    """
    Async TTS synthesis using Edge TTS.
    voice_params must contain: voice, rate, pitch, volume
    """
    voice = voice_params.get("voice", "en-US-GuyNeural")
    rate = voice_params.get("rate", "+0%")
    pitch = voice_params.get("pitch", "+0%")
    volume = voice_params.get("volume", "+0%")

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume
    )

    await communicate.save(output_path)
    return output_path


def synthesize_speech(
    text: str,
    voice_params: Dict[str, str],
    output_dir: str = "outputs",
    filename: Optional[str] = None
) -> str:
    """
    Synchronous wrapper for Edge TTS synthesis.
    Returns the saved audio file path.
    """
    if not text or not text.strip():
        raise ValueError("Input text is empty.")

    _ensure_outputs_dir(output_dir)

    if filename is None:
        filename = _safe_filename("empathy")

    output_path = os.path.join(output_dir, filename)

    # Windows-safe asyncio execution
    try:
        asyncio.run(_synthesize_async(text, voice_params, output_path))
    except RuntimeError:
        # If already inside an event loop (rare in notebooks),
        # use a new loop.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_synthesize_async(text, voice_params, output_path))
        loop.close()

    return output_path
