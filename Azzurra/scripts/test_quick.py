"""
Test rapido Azzurra-voice con testo di 30 secondi
"""
import os
import sys
import time
import torch
import soundfile as sf
from transformers import AutoProcessor, CsmForConditionalGeneration
from datetime import datetime

# Fix per UTF-8 su Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def test_azzurra_30sec():
    """Test con testo di 30 secondi"""

    # Leggi testo di test
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    testo_file = os.path.join(base_dir, "testo_test_30sec.txt")

    with open(testo_file, 'r', encoding='utf-8') as f:
        testo = f.read().strip()

    print("=" * 70)
    print("🎯 TEST RAPIDO AZZURRA-VOICE - 30 SECONDI")
    print("=" * 70)
    print(f"\n📝 Testo ({len(testo)} caratteri):")
    print(f"   {testo[:100]}...")

    # Setup
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "azzurra-voice")
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_output")
    os.makedirs(output_dir, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n🖥️  Device: {device}")

    # Carica modello
    print(f"\n🔄 Caricamento modello Cartesia CSM...")
    print(f"   (Modello: cartesia/azzurra-voice - 2B parametri)")
    load_start = time.time()

    try:
        processor = AutoProcessor.from_pretrained(model_path)
        model = CsmForConditionalGeneration.from_pretrained(model_path).to(device)
        load_time = time.time() - load_start
        print(f"✅ Modello caricato in {load_time:.2f}s")

    except Exception as e:
        print(f"❌ Errore caricamento modello: {e}")
        print("\n💡 Possibili cause:")
        print("   1. Modello non scaricato: esegui python scripts/download_model.py")
        print("   2. Libreria CSM non installata: pip install transformers>=4.30.0")
        return

    # Sintesi
    print(f"\n🎤 Sintesi in corso...")
    print("   Nota: Usando chat template per sintesi italiana")

    synth_start = time.time()

    try:
        # Prepara conversazione con chat template
        conversation = [
            {"role": "user", "content": [{"type": "text", "text": testo}]},
        ]

        # Applica chat template
        inputs = processor.apply_chat_template(
            conversation,
            tokenize=True,
            return_dict=True,
        ).to(device)

        # Genera audio con output_audio=True
        with torch.no_grad():
            audio_output = model.generate(**inputs, output_audio=True)

        synth_time = time.time() - synth_start

        # Estrai waveform
        audio = audio_output[0].cpu().numpy()
        sample_rate = 24000  # Azzurra-voice usa 24kHz

    except Exception as e:
        print(f"❌ Errore durante la sintesi: {e}")
        print("\n💡 Il modello CSM potrebbe richiedere configurazione specifica")
        import traceback
        traceback.print_exc()
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"azzurra_30sec_{timestamp}.wav")
    sf.write(output_file, audio, sample_rate)

    # Metriche
    audio_duration = len(audio) / sample_rate
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
    test_azzurra_30sec()
