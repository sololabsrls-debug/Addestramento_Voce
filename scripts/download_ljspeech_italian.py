#!/usr/bin/env python3
"""
Download e preparazione dataset LJSpeech-Italian per training Piper TTS
Risolve errore: ImportError: To support decoding audio data, please install 'torchcodec'
"""

import os
import sys
from datasets import load_dataset
from tqdm import tqdm
import soundfile as sf

def install_torchcodec():
    """Installa torchcodec se mancante"""
    try:
        import torchcodec
        print("✅ torchcodec già installato")
    except ImportError:
        print("📦 Installazione torchcodec...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "torchcodec"])
        print("✅ torchcodec installato")

def download_ljspeech_italian(output_dir="/content/drive/MyDrive/piper_training/dataset/ljspeech_italian"):
    """
    Scarica e prepara dataset LJSpeech-Italian

    Args:
        output_dir: Directory di output (default: Google Drive path per Colab)
    """
    print("="*60)
    print("  DOWNLOAD LJSPEECH-IT")
    print("="*60)
    print()

    # Installa torchcodec
    install_torchcodec()

    # Scarica dataset
    print("📥 Scaricamento dataset...")
    dataset = load_dataset("sololabs/ljspeech-italian", split="train")
    print(f"✅ Dataset caricato: {len(dataset)} campioni")

    # Crea directory
    wavs_dir = os.path.join(output_dir, "wavs")
    os.makedirs(wavs_dir, exist_ok=True)

    print(f"\n💾 Salvataggio su Google Drive...")
    print(f"📁 Percorso: {output_dir}")

    # Prepara metadata
    metadata_lines = []
    total = len(dataset)

    for idx in tqdm(range(total), desc="Salvando audio"):
        item = dataset[idx]

        # Salva audio
        audio_filename = f"LJ_{idx:06d}.wav"
        audio_path = os.path.join(wavs_dir, audio_filename)

        # Estrai audio array e sample rate
        audio_data = item['audio']
        sf.write(audio_path, audio_data['array'], audio_data['sampling_rate'])

        # Aggiungi a metadata
        text = item['sentence']
        metadata_lines.append(f"{audio_filename}|{text}")

    # Salva metadata.csv
    metadata_path = os.path.join(output_dir, "metadata.csv")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(metadata_lines))

    print(f"\n✅ Completato!")
    print(f"   📊 {total} file audio salvati")
    print(f"   📄 metadata.csv creato")
    print(f"   💾 Totale: ~{total * 0.5:.1f} MB")

    return output_dir, metadata_path

if __name__ == "__main__":
    # Parse argomenti
    import argparse
    parser = argparse.ArgumentParser(description="Download LJSpeech-Italian dataset")
    parser.add_argument(
        "--output-dir",
        default="/content/drive/MyDrive/piper_training/dataset/ljspeech_italian",
        help="Directory di output"
    )
    args = parser.parse_args()

    # Esegui download
    download_ljspeech_italian(args.output_dir)
