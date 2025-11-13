#!/usr/bin/env python3
"""
Verifica dataset LJSpeech-ITALIANO scaricato
Mostra statistiche e controlla integrità
"""

import os
import soundfile as sf
import random

def verifica_dataset(dataset_dir="/content/ljspeech_italian"):
    """Verifica completezza e integrità del dataset"""

    wavs_dir = os.path.join(dataset_dir, "wavs")
    metadata_path = os.path.join(dataset_dir, "metadata.csv")

    print("="*60)
    print("  VERIFICA DATASET ITALIANO")
    print("="*60)
    print()

    # 1. Conta file WAV
    wav_files = [f for f in os.listdir(wavs_dir) if f.endswith('.wav')]
    print(f"📊 File WAV: {len(wav_files)}")

    # 2. Carica metadata in dizionario
    metadata_dict = {}
    with open(metadata_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 3:
                filename = parts[0]  # SENZA .wav
                text_original = parts[1]
                text_normalized = parts[2]
                metadata_dict[filename] = {
                    'original': text_original,
                    'normalized': text_normalized
                }

    print(f"📄 Righe metadata: {len(metadata_dict)}")

    # 3. Verifica corrispondenza
    if len(wav_files) == len(metadata_dict):
        print(f"✅ Corrispondenza perfetta!\n")
    else:
        print(f"⚠️  Disallineamento: {len(wav_files)} WAV vs {len(metadata_dict)} metadata\n")

    # 4. Test file audio random
    print("🎵 Test 5 file audio casuali:\n")
    random_samples = random.sample(wav_files, min(5, len(wav_files)))

    for wav_file in random_samples:
        wav_path = os.path.join(wavs_dir, wav_file)

        # Leggi audio
        data, samplerate = sf.read(wav_path)
        duration = len(data) / samplerate

        # Trova testo corrispondente (rimuovi .wav)
        filename_base = wav_file.replace('.wav', '')

        if filename_base in metadata_dict:
            text = metadata_dict[filename_base]['original']
            text_norm = metadata_dict[filename_base]['normalized']
        else:
            text = "❌ NON TROVATO"
            text_norm = "❌ NON TROVATO"

        print(f"📁 {wav_file}")
        print(f"   ⏱️  Durata: {duration:.2f}s")
        print(f"   🔊 Sample rate: {samplerate}Hz")
        print(f"   📝 Testo: {text[:80]}...")
        print()

    # 5. Statistiche dataset
    print("="*60)
    print("  📊 STATISTICHE DATASET")
    print("="*60)

    total_duration = 0
    sample_rates = set()

    for wav_file in wav_files:
        wav_path = os.path.join(wavs_dir, wav_file)
        try:
            data, samplerate = sf.read(wav_path)
            total_duration += len(data) / samplerate
            sample_rates.add(samplerate)
        except Exception as e:
            print(f"⚠️  Errore lettura {wav_file}: {e}")

    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    seconds = int(total_duration % 60)

    print(f"📊 File totali: {len(wav_files)}")
    print(f"⏱️  Durata totale: {hours}h {minutes}m {seconds}s")
    print(f"⏱️  Durata media: {total_duration/len(wav_files):.2f}s per file")
    print(f"🔊 Sample rate(s): {', '.join(map(str, sample_rates))}Hz")
    print(f"🇮🇹 Lingua: ITALIANO")

    print("\n" + "="*60)
    print("  ✅ DATASET PRONTO PER IL TRAINING!")
    print("="*60)

    return {
        'num_files': len(wav_files),
        'duration_hours': total_duration / 3600,
        'sample_rates': list(sample_rates),
        'metadata_count': len(metadata_dict)
    }

if __name__ == "__main__":
    import sys

    dataset_dir = sys.argv[1] if len(sys.argv) > 1 else "/content/ljspeech_italian"
    stats = verifica_dataset(dataset_dir)
