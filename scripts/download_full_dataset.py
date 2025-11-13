#!/usr/bin/env python3
"""
Download COMPLETO del dataset LJSpeech-Italian (tutti i 5856 file)
Ottimizzato con streaming mode per non saturare la RAM
"""

import os
import sys
from pathlib import Path

# Aggiungi directory scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from download_ljspeech_italian import download_ljspeech_italian

if __name__ == "__main__":
    print("="*60)
    print("  DOWNLOAD COMPLETO LJSPEECH-ITALIAN")
    print("  ⚠️  Scaricamento di TUTTI i 5856 file")
    print("="*60)
    print()

    # Configurazione
    OUTPUT_DIR = "/content/ljspeech_italian"  # Cambia se vuoi altra directory
    DATASET_NAME = "z-uo/female-LJSpeech-italian"  # 5856 file, voce femminile

    print(f"📁 Directory output: {OUTPUT_DIR}")
    print(f"📦 Dataset: {DATASET_NAME}")
    print(f"🔢 File da scaricare: TUTTI (5856)")
    print()

    response = input("Continuare? (s/n): ")
    if response.lower() != 's':
        print("❌ Download annullato")
        sys.exit(0)

    # Avvia download COMPLETO (max_samples=None)
    output_dir, metadata_path = download_ljspeech_italian(
        output_dir=OUTPUT_DIR,
        dataset_name=DATASET_NAME,
        max_samples=None,  # TUTTI I FILE!
        streaming=True     # Risparmia RAM
    )

    print()
    print("="*60)
    print("  ✅ DOWNLOAD COMPLETATO!")
    print("="*60)
    print(f"📁 Directory: {output_dir}")
    print(f"📄 Metadata: {metadata_path}")
