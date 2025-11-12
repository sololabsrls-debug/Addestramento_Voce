#!/usr/bin/env python3
"""
Coqui XTTS v2 - Script di generazione audio
"""

from TTS.api import TTS
import torch

# Testo di test (30 secondi circa)
TEST_TEXT = """Buongiorno, benvenuti nel nostro sistema di assistenza telefonica.
Sono un assistente virtuale e oggi vi parlerò della sintesi vocale in italiano.
La tecnologia text-to-speech permette di convertire il testo scritto in parlato naturale.
Questo modello è stato addestrato su migliaia di ore di audio in lingua italiana.
Posso gestire numeri come 12345, date come il 23 maggio 2025, e nomi propri come Milano e Bianchi.
La qualità della voce dipende dall'architettura del modello e dai dati di addestramento.
Grazie per l'ascolto, arrivederci!"""

def generate_audio_file():
    print("Caricamento Coqui XTTS v2...")
    print("(Questo può richiedere qualche minuto al primo avvio)")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Utilizzo device: {device}")

    # Inizializza TTS con XTTS v2
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(device)

    print("\nGenerazione audio con XTTS v2...")

    output_path = "output.wav"

    # Genera audio in italiano
    # XTTS v2 supporta voice cloning, ma qui usiamo la voce di default
    tts.tts_to_file(
        text=TEST_TEXT,
        language="it",
        file_path=output_path
    )

    print(f"✓ Audio generato: {output_path}")

    # Info sul file
    import wave
    with wave.open(output_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
        print(f"  Durata: {duration:.2f} secondi")
        print(f"  Sample rate: {rate} Hz")

if __name__ == "__main__":
    generate_audio_file()
