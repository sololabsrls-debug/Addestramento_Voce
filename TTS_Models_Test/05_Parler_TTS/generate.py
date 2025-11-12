#!/usr/bin/env python3
"""
Parler-TTS - Script di generazione audio
"""

import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

# Testo di test (30 secondi circa)
TEST_TEXT = """Buongiorno, benvenuti nel nostro sistema di assistenza telefonica.
Sono un assistente virtuale e oggi vi parlerò della sintesi vocale in italiano.
La tecnologia text-to-speech permette di convertire il testo scritto in parlato naturale.
Questo modello è stato addestrato su migliaia di ore di audio in lingua italiana.
Posso gestire numeri come 12345, date come il 23 maggio 2025, e nomi propri come Milano e Bianchi.
La qualità della voce dipende dall'architettura del modello e dai dati di addestramento.
Grazie per l'ascolto, arrivederci!"""

def generate_audio_file():
    print("Caricamento modelli Parler-TTS...")
    print("(Questo può richiedere qualche minuto al primo avvio)")

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Utilizzo device: {device}")

    # Carica il modello multilingua
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        "parler-tts/parler-tts-mini-v1"
    ).to(device)

    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

    print("\nGenerazione audio con Parler-TTS...")

    # Descrizione della voce desiderata
    description = "A clear, professional Italian voice speaks with neutral tone and good articulation."

    # Tokenizza
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(TEST_TEXT, return_tensors="pt").input_ids.to(device)

    # Genera audio
    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    # Salva come WAV
    output_path = "output.wav"
    sample_rate = model.config.sampling_rate
    sf.write(output_path, audio_arr, sample_rate)

    duration = len(audio_arr) / sample_rate
    print(f"✓ Audio generato: {output_path}")
    print(f"  Durata: {duration:.2f} secondi")
    print(f"  Sample rate: {sample_rate} Hz")

if __name__ == "__main__":
    generate_audio_file()
