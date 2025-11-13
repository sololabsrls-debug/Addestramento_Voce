#!/usr/bin/env python3
"""
DOWNLOAD DATASET ITALIANO - Memory-safe version
Usa lo script ottimizzato già presente nel repo
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
    print("  DOWNLOAD DATASET LJSpeech-ITALIANO")
    print("  Memory-safe con checkpoint system")
    print("="*60)
    print()

    # Configurazione
    OUTPUT_DIR = "/content/ljspeech_italian"
    DATASET_NAME = "z-uo/female-LJSpeech-italian"  # 5856 file, voce femminile

    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"📦 Dataset: {DATASET_NAME}")
    print(f"🇮🇹 Lingua: ITALIANO")
    print(f"🔢 File: TUTTI (5856)")
    print()
    print("✨ Funzionalità:")
    print("   ✅ Retry automatico con backoff esponenziale")
    print("   ✅ Checkpoint system (riprende se si interrompe)")
    print("   ✅ Garbage collection ogni 100 file")
    print("   ✅ Monitoraggio RAM in tempo reale")
    print("   ✅ Streaming mode (no memory overflow)")
    print()

    # Esegui download con tutte le ottimizzazioni
    try:
        output_dir, metadata_path = download_ljspeech_italian(
            output_dir=OUTPUT_DIR,
            dataset_name=DATASET_NAME,
            max_samples=None,      # TUTTI i file
            streaming=True,        # Streaming mode (memory-safe)
            resume=True            # Riprende da checkpoint se interrotto
        )

        print()
        print("="*60)
        print("  ✅ DOWNLOAD COMPLETATO!")
        print("="*60)
        print(f"📁 Directory: {output_dir}")
        print(f"📄 Metadata: {metadata_path}")

        # Verifica che sia ITALIANO
        print()
        print("📝 Verifica lingua (prime 3 righe):")
        with open(metadata_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= 3:
                    break
                # Estrai solo il testo (dopo il pipe)
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    print(f"   {parts[0]}: {parts[1][:80]}...")

    except KeyboardInterrupt:
        print("\n⚠️  Download interrotto dall'utente")
        print("💡 Riesegui lo script per riprendere dal checkpoint")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        print("\n💡 Suggerimenti:")
        print("   1. Verifica connessione internet")
        print("   2. Controlla spazio disco disponibile")
        print("   3. Riavvia e riesegui (riprenderà dal checkpoint)")
        sys.exit(1)
