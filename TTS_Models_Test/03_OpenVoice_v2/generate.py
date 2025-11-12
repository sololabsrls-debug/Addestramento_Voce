#!/usr/bin/env python3
"""
OpenVoice v2 - Script di generazione audio
"""

import os
import sys
import torch

# Aggiungi il path di OpenVoice
sys.path.append('OpenVoice')

from openvoice import se_extractor
from openvoice.api import ToneColorConverter

# Testo di test (30 secondi circa)
TEST_TEXT = """Buongiorno, benvenuti nel nostro sistema di assistenza telefonica.
Sono un assistente virtuale e oggi vi parlerò della sintesi vocale in italiano.
La tecnologia text-to-speech permette di convertire il testo scritto in parlato naturale.
Questo modello è stato addestrato su migliaia di ore di audio in lingua italiana.
Posso gestire numeri come 12345, date come il 23 maggio 2025, e nomi propri come Milano e Bianchi.
La qualità della voce dipende dall'architettura del modello e dai dati di addestramento.
Grazie per l'ascolto, arrivederci!"""

def generate_audio_file():
    print("Caricamento OpenVoice v2...")

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Utilizzo device: {device}")

    # Percorsi
    ckpt_converter = 'OpenVoice/checkpoints/converter'

    if not os.path.exists(ckpt_converter):
        print("ERRORE: Modelli non trovati. Esegui prima setup.sh")
        return

    # Inizializza il tone color converter
    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

    print("\nGenerazione audio con OpenVoice v2...")

    # Per OpenVoice v2, abbiamo bisogno di un audio base e poi applichiamo tone color
    # In questo caso useremo il base TTS per generare l'audio
    # Nota: OpenVoice v2 è principalmente per voice cloning/conversion

    print("NOTA: OpenVoice v2 è ottimizzato per voice cloning/conversion")
    print("Per generare audio, richiede un audio base da convertire")
    print("Considera l'uso di XTTS o altri modelli per sintesi diretta")

    output_path = "output.wav"

    # Genera un placeholder
    print(f"✓ Per usare OpenVoice v2, fornisci un audio di riferimento per voice cloning")

if __name__ == "__main__":
    generate_audio_file()
