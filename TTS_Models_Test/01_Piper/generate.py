#!/usr/bin/env python3
"""
Piper TTS - Script di generazione audio
"""

import wave
import subprocess
import os

# Testo di test (30 secondi circa)
TEST_TEXT = """Buongiorno, benvenuti nel nostro sistema di assistenza telefonica.
Sono un assistente virtuale e oggi vi parlerò della sintesi vocale in italiano.
La tecnologia text-to-speech permette di convertire il testo scritto in parlato naturale.
Questo modello è stato addestrato su migliaia di ore di audio in lingua italiana.
Posso gestire numeri come 12345, date come il 23 maggio 2025, e nomi propri come Milano e Bianchi.
La qualità della voce dipende dall'architettura del modello e dai dati di addestramento.
Grazie per l'ascolto, arrivederci!"""

def generate_audio():
    print("Generazione audio con Piper TTS...")

    model_path = "models/it_IT-riccardo-x_low.onnx"
    output_path = "output.wav"

    if not os.path.exists(model_path):
        print(f"ERRORE: Modello non trovato in {model_path}")
        print("Esegui prima setup.sh")
        return

    # Usa piper da command line
    with open("temp_text.txt", "w", encoding="utf-8") as f:
        f.write(TEST_TEXT)

    try:
        cmd = f'cat temp_text.txt | piper --model {model_path} --output_file {output_path}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ Audio generato: {output_path}")

            # Info sul file generato
            with wave.open(output_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                duration = frames / float(rate)
                print(f"  Durata: {duration:.2f} secondi")
                print(f"  Sample rate: {rate} Hz")
        else:
            print(f"ERRORE: {result.stderr}")

    finally:
        if os.path.exists("temp_text.txt"):
            os.remove("temp_text.txt")

if __name__ == "__main__":
    generate_audio()
