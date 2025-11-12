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

def download_ljspeech_italian(output_dir="/content/drive/MyDrive/piper_training/dataset/ljspeech_italian",
                              dataset_name="z-uo/female-LJSpeech-italian",
                              max_samples=None,
                              streaming=True):
    """
    Scarica e prepara dataset LJSpeech-Italian

    Args:
        output_dir: Directory di output (default: Google Drive path per Colab)
        dataset_name: Nome dataset Hugging Face
                     - z-uo/female-LJSpeech-italian (8h 23m, voce femminile)
                     - z-uo/male-LJSpeech-italian (31h 45m, voce maschile)
        max_samples: Numero massimo di sample da processare (None = tutti)
        streaming: Usa streaming mode per risparmiare memoria (default: True)
    """
    print("="*60)
    print("  DOWNLOAD LJSPEECH-IT" + (" - STREAMING MODE" if streaming else ""))
    print("="*60)
    print()

    # Installa torchcodec
    install_torchcodec()

    # Scarica dataset
    print(f"📥 Scaricamento dataset: {dataset_name}...")
    if streaming:
        print("💡 Uso streaming mode per risparmiare memoria")

    dataset = load_dataset(dataset_name, split="train", streaming=streaming)

    if not streaming:
        print(f"✅ Dataset caricato: {len(dataset)} campioni")
    else:
        print(f"✅ Dataset pronto (streaming mode)")

    # Crea directory
    wavs_dir = os.path.join(output_dir, "wavs")
    os.makedirs(wavs_dir, exist_ok=True)

    print(f"\n💾 Salvataggio su Google Drive...")
    print(f"📁 Percorso: {output_dir}")

    # Prepara metadata
    metadata_lines = []
    processed = 0

    # Processa sample
    import gc
    for idx, item in enumerate(tqdm(dataset, desc="Salvando audio")):
        try:
            # Limita numero di sample se richiesto
            if max_samples and idx >= max_samples:
                print(f"\n⏸️  Limite raggiunto: {max_samples} sample processati")
                break

            # Salva audio
            audio_filename = f"LJ_{idx:06d}.wav"
            audio_path = os.path.join(wavs_dir, audio_filename)

            # Estrai audio array e sample rate
            audio_data = item['audio']
            sf.write(audio_path, audio_data['array'], audio_data['sampling_rate'])

            # Aggiungi a metadata
            text = item['text']
            metadata_lines.append(f"{audio_filename}|{text}")

            processed += 1

            # Libera memoria ogni 100 file
            if streaming and processed % 100 == 0:
                gc.collect()

        except Exception as e:
            print(f"\n⚠️  Errore sample {idx}: {e}")
            continue

    # Salva metadata.csv
    metadata_path = os.path.join(output_dir, "metadata.csv")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(metadata_lines))

    print(f"\n✅ Completato!")
    print(f"   📊 {processed} file audio salvati")
    print(f"   📄 metadata.csv creato")
    print(f"   💾 Totale: ~{processed * 0.5:.1f} MB")

    # Libera memoria finale
    if streaming:
        import gc
        del dataset
        gc.collect()

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
    parser.add_argument(
        "--dataset",
        default="z-uo/female-LJSpeech-italian",
        choices=["z-uo/female-LJSpeech-italian", "z-uo/male-LJSpeech-italian"],
        help="Dataset da scaricare: female (8h) o male (31h)"
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Numero massimo di sample da processare (default: tutti)"
    )
    parser.add_argument(
        "--no-streaming",
        action="store_true",
        help="Disabilita streaming mode (richiede più RAM)"
    )
    args = parser.parse_args()

    # Esegui download
    download_ljspeech_italian(
        output_dir=args.output_dir,
        dataset_name=args.dataset,
        max_samples=args.max_samples,
        streaming=not args.no_streaming
    )
