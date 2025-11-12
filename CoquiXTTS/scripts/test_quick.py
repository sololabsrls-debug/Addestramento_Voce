"""
Test rapido Coqui XTTS v2 con testo di 30 secondi
"""
import os
import sys
import time
import torch
import soundfile as sf
from TTS.api import TTS
from datetime import datetime

# Fix per UTF-8 su Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def test_xtts_30sec():
    """Test con testo di 30 secondi"""

    # Leggi testo di test
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    testo_file = os.path.join(base_dir, "testo_test_30sec.txt")

    with open(testo_file, 'r', encoding='utf-8') as f:
        testo = f.read().strip()

    print("=" * 70)
    print("🎯 TEST RAPIDO COQUI XTTS v2 - 30 SECONDI")
    print("=" * 70)
    print(f"\n📝 Testo ({len(testo)} caratteri):")
    print(f"   {testo[:100]}...")

    # Setup
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_output")
    os.makedirs(output_dir, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n🖥️  Device: {device}")

    # Carica modello
    print(f"\n🔄 Caricamento modello XTTS v2...")
    print("   (Primo avvio: scarica modello automaticamente)")
    load_start = time.time()

    try:
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        load_time = time.time() - load_start
        print(f"✅ Modello caricato in {load_time:.2f}s")

    except Exception as e:
        print(f"❌ Errore caricamento modello: {e}")
        return

    # Sintesi
    print(f"\n🎤 Sintesi in corso...")
    print("   Nota: XTTS v2 utilizza voice cloning zero-shot")

    # Cerca file audio di riferimento convertito
    speaker_wav = os.path.join(base_dir, "voci_riferimento", "voce_riferimento_converted.wav")

    if not os.path.exists(speaker_wav):
        print(f"❌ File voce di riferimento non trovato: {speaker_wav}")
        print("   Inserisci un file audio nella cartella voci_riferimento/")
        return

    print(f"🎭 Usando voce campione: {os.path.basename(speaker_wav)}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"xtts_30sec_{timestamp}.wav")

    synth_start = time.time()

    try:
        # Sintesi con speaker wav reale
        tts.tts_to_file(
            text=testo,
            file_path=output_file,
            speaker_wav=speaker_wav,
            language="it"
        )

    except Exception as e:
        print(f"❌ Errore sintesi: {e}")
        import traceback
        traceback.print_exc()
        return

    synth_time = time.time() - synth_start

    # Metriche
    audio_data, sample_rate = sf.read(output_file)
    audio_duration = len(audio_data) / sample_rate
    rtf = synth_time / audio_duration if audio_duration > 0 else 0

    print("\n" + "=" * 70)
    print("📊 RISULTATI")
    print("=" * 70)
    print(f"⏱️  Tempo sintesi: {synth_time:.3f}s")
    print(f"🎵 Durata audio: {audio_duration:.3f}s")
    print(f"📊 RTF: {rtf:.3f}x")
    print(f"🔊 Sample rate: {sample_rate} Hz")
    print(f"💾 File salvato: {output_file}")
    print(f"\n✅ Test completato!")

if __name__ == "__main__":
    test_xtts_30sec()
