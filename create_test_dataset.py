#!/usr/bin/env python3
"""
Crea un dataset di test per verificare lo script verify_dataset.py
Genera file WAV silenti nel formato corretto
"""

import os
import wave
import struct
from pathlib import Path

def create_silent_wav(filename, duration_sec, sample_rate=22050):
    """Crea un file WAV silente con i parametri specificati"""
    num_samples = int(duration_sec * sample_rate)

    with wave.open(filename, 'wb') as wav_file:
        # Imposta parametri: 1 canale (mono), 2 bytes per sample (16-bit), sample rate
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        # Scrivi campioni silenziosi (valore 0)
        for _ in range(num_samples):
            wav_file.writeframes(struct.pack('<h', 0))

def create_test_dataset(base_dir="test_dataset"):
    """Crea un dataset di test completo"""

    base_path = Path(base_dir)
    wavs_dir = base_path / "wavs"

    # Crea directory
    wavs_dir.mkdir(parents=True, exist_ok=True)

    print(f"Creando dataset di test in: {base_path.absolute()}")

    # Dati di test
    test_data = [
        # (filename, duration, text)
        ("audio_001.wav", 4.5, "Questo è un esempio di testo per il training."),
        ("audio_002.wav", 5.2, "L'addestramento richiede file WAV in formato corretto."),
        ("audio_003.wav", 3.8, "La qualità dell'audio è importante per i risultati."),
        ("audio_004.wav", 6.1, "Ogni file deve avere la trascrizione corrispondente."),
        ("audio_005.wav", 4.0, "Il dataset deve essere bilanciato e vario."),
        # Casi problematici per test
        ("audio_006.wav", 2.5, "Troppo corto"),  # Warning: durata non ideale
        ("audio_007.wav", 8.5, "Questo file è un po' più lungo del normale ma ancora accettabile."),  # Warning
        ("audio_008.wav", 5.5, "Un altro esempio di audio per il training della voce."),
        ("audio_009.wav", 4.8, "I modelli TTS imparano dai dati di addestramento."),
        ("audio_010.wav", 5.0, "Ricorda di verificare sempre il dataset prima di iniziare."),
    ]

    # Crea file WAV
    print("\nCreando file WAV:")
    for filename, duration, _ in test_data:
        wav_path = wavs_dir / filename
        create_silent_wav(str(wav_path), duration)
        print(f"  ✓ {filename} ({duration}s)")

    # Crea metadata.csv
    metadata_path = base_path / "metadata.csv"
    print(f"\nCreando {metadata_path}:")

    with open(metadata_path, 'w', encoding='utf-8') as f:
        for filename, _, text in test_data:
            f.write(f"wavs/{filename}|{text}\n")

    print(f"  ✓ {len(test_data)} righe scritte")

    # Crea anche un esempio con errori
    error_dataset = base_path.parent / "test_dataset_errors"
    error_wavs = error_dataset / "wavs"
    error_wavs.mkdir(parents=True, exist_ok=True)

    # File con problemi
    print(f"\nCreando dataset con errori in: {error_dataset.absolute()}")

    # WAV troppo corto
    create_silent_wav(str(error_wavs / "short.wav"), 0.5, sample_rate=22050)
    print("  ✓ short.wav (0.5s - troppo corto)")

    # WAV troppo lungo
    create_silent_wav(str(error_wavs / "long.wav"), 12.0, sample_rate=22050)
    print("  ✓ long.wav (12.0s - troppo lungo)")

    # WAV con sample rate errato
    create_silent_wav(str(error_wavs / "wrong_sr.wav"), 4.0, sample_rate=44100)
    print("  ✓ wrong_sr.wav (44100Hz - sample rate errato)")

    # WAV ok
    create_silent_wav(str(error_wavs / "ok.wav"), 4.5, sample_rate=22050)
    print("  ✓ ok.wav (4.5s - OK)")

    # Metadata con errori
    error_metadata = error_dataset / "metadata.csv"
    with open(error_metadata, 'w', encoding='utf-8') as f:
        f.write("wavs/short.wav|Testo troppo corto\n")
        f.write("wavs/long.wav|Questo file è molto lungo e supera i limiti consigliati\n")
        f.write("wavs/wrong_sr.wav|File con sample rate sbagliato\n")
        f.write("wavs/ok.wav|Questo file è corretto\n")
        f.write("wavs/missing.wav|Questo file non esiste\n")  # Errore: file mancante
        f.write("wavs/empty.wav|\n")  # Errore: testo vuoto

    print(f"  ✓ metadata.csv con alcuni errori")

    # Riepilogo
    print("\n" + "="*50)
    print("Dataset di test creati!")
    print("="*50)
    print(f"\n1. Dataset CORRETTO:")
    print(f"   {base_path.absolute()}")
    print(f"   - {len(test_data)} file WAV")
    print(f"   - Tutti i file sono validi")
    print(f"\n2. Dataset con ERRORI:")
    print(f"   {error_dataset.absolute()}")
    print(f"   - File con durate errate")
    print(f"   - File con sample rate errato")
    print(f"   - Metadata con problemi")
    print(f"\nPer testare lo script di verifica:")
    print(f"  python verify_dataset.py {base_path}")
    print(f"  python verify_dataset.py {error_dataset}")

if __name__ == "__main__":
    create_test_dataset()
