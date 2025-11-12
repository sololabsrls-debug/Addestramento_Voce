#!/usr/bin/env python3
"""
Bark TTS - Script di generazione audio
"""

import numpy as np
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import os

# Testo di test (30 secondi circa)
TEST_TEXT = """Buongiorno, benvenuti nel nostro sistema di assistenza telefonica.
Sono un assistente virtuale e oggi vi parlerò della sintesi vocale in italiano.
La tecnologia text-to-speech permette di convertire il testo scritto in parlato naturale.
Questo modello è stato addestrato su migliaia di ore di audio in lingua italiana.
Posso gestire numeri come 12345, date come il 23 maggio 2025, e nomi propri come Milano e Bianchi.
La qualità della voce dipende dall'architettura del modello e dai dati di addestramento.
Grazie per l'ascolto, arrivederci!"""

def generate_audio_file():
    print("Caricamento modelli Bark...")
    print("(Questo può richiedere qualche minuto al primo avvio)")

    # Precarica i modelli
    preload_models()

    print("\nGenerazione audio con Bark TTS...")

    # Genera audio - usa speaker italiano
    # v2/it_speaker_X per voci italiane
    audio_array = generate_audio(TEST_TEXT, history_prompt="v2/it_speaker_6")

    # Salva come WAV
    output_path = "output.wav"
    write_wav(output_path, SAMPLE_RATE, audio_array)

    duration = len(audio_array) / SAMPLE_RATE
    print(f"✓ Audio generato: {output_path}")
    print(f"  Durata: {duration:.2f} secondi")
    print(f"  Sample rate: {SAMPLE_RATE} Hz")

if __name__ == "__main__":
    generate_audio_file()
