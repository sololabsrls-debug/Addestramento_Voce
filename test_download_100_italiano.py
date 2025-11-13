#!/usr/bin/env python3
"""
TEST RAPIDO - Scarica solo 100 file per verificare che funzioni
Prima di scaricare tutti i 5856 file
"""

import sys
import os
from pathlib import Path

# Aggiungi directory scripts al path
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

# Import dello script ottimizzato
from download_ljspeech_italian import download_ljspeech_italian

if __name__ == "__main__":
    print("="*60)
    print("  TEST DOWNLOAD - 100 file ITALIANI")
    print("="*60)
    print()

    # Configurazione TEST
    OUTPUT_DIR = "/content/ljspeech_italian_test"
    DATASET_NAME = "z-uo/female-LJSpeech-italian"

    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"📦 Dataset: {DATASET_NAME}")
    print(f"🇮🇹 Lingua: ITALIANO")
    print(f"🔢 File: 100 (test rapido)")
    print(f"⏱️  Tempo stimato: ~2-3 minuti")
    print()

    try:
        output_dir, metadata_path = download_ljspeech_italian(
            output_dir=OUTPUT_DIR,
            dataset_name=DATASET_NAME,
            max_samples=100,       # Solo 100 file per test
            streaming=True,
            resume=True
        )

        print()
        print("="*60)
        print("  ✅ TEST COMPLETATO!")
        print("="*60)
        print(f"📁 Directory: {output_dir}")
        print(f"📄 Metadata: {metadata_path}")

        # Verifica che sia ITALIANO
        print()
        print("🇮🇹 VERIFICA LINGUA (prime 5 righe):")
        print()
        with open(metadata_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= 5:
                    break
                # Estrai solo il testo (dopo il pipe)
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    text = parts[1]
                    print(f"   [{i+1}] {text[:100]}{'...' if len(text) > 100 else ''}")

        print()
        print("💡 Se il testo sopra è in ITALIANO ✅")
        print("   Esegui: python download_dataset_italiano.py")
        print("   per scaricare tutti i 5856 file")

    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)
