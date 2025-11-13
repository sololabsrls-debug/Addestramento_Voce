#!/usr/bin/env python3
"""
Download e preparazione dataset LJSpeech-Italian per training Piper TTS
Con gestione rate limits, retry logic e checkpoint system
"""

import os
import sys
import time
import json
from datasets import load_dataset
from tqdm import tqdm
import soundfile as sf
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException

# Carica variabili d'ambiente dal file .env
load_dotenv()

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

def load_checkpoint(checkpoint_path):
    """Carica checkpoint se esistente"""
    if os.path.exists(checkpoint_path):
        try:
            with open(checkpoint_path, 'r') as f:
                checkpoint = json.load(f)
            print(f"📋 Checkpoint trovato: {checkpoint['processed']} file già processati")
            return checkpoint
        except Exception as e:
            print(f"⚠️  Errore lettura checkpoint: {e}")
    return {'processed': 0, 'files': [], 'metadata': []}

def save_checkpoint(checkpoint_path, checkpoint_data):
    """Salva checkpoint"""
    try:
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint_data, f)
    except Exception as e:
        print(f"⚠️  Errore salvataggio checkpoint: {e}")

def retry_with_backoff(func, max_retries=5, initial_wait=2, max_wait=300):
    """
    Esegue una funzione con retry logic e backoff esponenziale

    Args:
        func: Funzione da eseguire
        max_retries: Numero massimo di tentativi
        initial_wait: Tempo di attesa iniziale in secondi
        max_wait: Tempo massimo di attesa in secondi
    """
    wait_time = initial_wait

    for attempt in range(max_retries):
        try:
            return func()
        except RequestException as e:
            error_msg = str(e).lower()

            # Gestisci rate limiting
            if 'rate limit' in error_msg or '429' in error_msg:
                print(f"\n⚠️  Rate limit! Pausa {wait_time} secondi...")
                time.sleep(wait_time)
                wait_time = min(wait_time * 2, max_wait)
                continue

            # Gestisci errori di rete
            if 'connection' in error_msg or 'timeout' in error_msg:
                if attempt < max_retries - 1:
                    print(f"\n⚠️  Errore rete, retry {attempt+1}/{max_retries} tra {wait_time}s...")
                    time.sleep(wait_time)
                    wait_time = min(wait_time * 2, max_wait)
                    continue

            # Altri errori
            if attempt < max_retries - 1:
                print(f"\n⚠️  Errore: {e}, retry {attempt+1}/{max_retries}...")
                time.sleep(wait_time)
                wait_time = min(wait_time * 2, max_wait)
            else:
                raise
        except Exception as e:
            # Per altri tipi di eccezioni, ritenta solo poche volte
            if attempt < 2:
                print(f"\n⚠️  Errore: {e}, retry {attempt+1}/3...")
                time.sleep(initial_wait)
            else:
                raise

    raise Exception(f"Fallito dopo {max_retries} tentativi")

def download_ljspeech_italian(output_dir="/content/drive/MyDrive/piper_training/dataset/ljspeech_italian",
                              dataset_name="z-uo/female-LJSpeech-italian",
                              max_samples=None,
                              streaming=True,
                              resume=True):
    """
    Scarica e prepara dataset LJSpeech-Italian con retry logic e checkpoint

    Args:
        output_dir: Directory di output (default: Google Drive path per Colab)
        dataset_name: Nome dataset Hugging Face
                     - z-uo/female-LJSpeech-italian (8h 23m, voce femminile)
                     - z-uo/male-LJSpeech-italian (31h 45m, voce maschile)
        max_samples: Numero massimo di sample da processare (None = tutti)
        streaming: Usa streaming mode per risparmiare memoria (default: True)
        resume: Riprende da checkpoint se disponibile (default: True)
    """
    print("="*60)
    print("  DOWNLOAD LJSPEECH-IT" + (" - STREAMING MODE" if streaming else ""))
    print("="*60)
    print()

    # Installa torchcodec
    install_torchcodec()

    # Ottieni token Hugging Face
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("⚠️  ATTENZIONE: HF_TOKEN non trovato nel file .env")
        print("   Alcuni dataset potrebbero richiedere autenticazione")
    else:
        print(f"✅ Token HF trovato: {hf_token[:10]}...")

    # Crea directory
    wavs_dir = os.path.join(output_dir, "wavs")
    os.makedirs(wavs_dir, exist_ok=True)

    # Carica checkpoint se richiesto
    checkpoint_path = os.path.join(output_dir, ".checkpoint.json")
    checkpoint = load_checkpoint(checkpoint_path) if resume else {'processed': 0, 'files': [], 'metadata': []}

    # Scarica dataset con retry
    print(f"\n📥 Scaricamento dataset: {dataset_name}...")
    if streaming:
        print("💡 Uso streaming mode per risparmiare memoria")

    def load_dataset_with_retry():
        return load_dataset(
            dataset_name,
            split="train",
            streaming=streaming,
            token=hf_token
        )

    try:
        dataset = retry_with_backoff(load_dataset_with_retry, max_retries=5, initial_wait=5)
    except Exception as e:
        print(f"\n❌ Errore caricamento dataset: {e}")
        print("💡 Suggerimenti:")
        print("   - Verifica connessione internet")
        print("   - Controlla che il token HF sia valido")
        print("   - Prova ad aumentare il timeout")
        raise

    if not streaming:
        print(f"✅ Dataset caricato: {len(dataset)} campioni")
    else:
        print(f"✅ Dataset pronto (streaming mode)")

    print(f"\n💾 Salvataggio file audio...")
    print(f"📁 Percorso: {output_dir}")

    # Prepara metadata
    metadata_lines = checkpoint.get('metadata', [])
    processed = checkpoint.get('processed', 0)
    start_idx = processed

    # Processa sample
    import gc
    import psutil

    # Skip file già processati
    dataset_iter = iter(dataset)
    for _ in range(start_idx):
        try:
            next(dataset_iter)
        except StopIteration:
            break

    print(f"📋 Riprendendo dal file {start_idx}...")

    consecutive_errors = 0
    max_consecutive_errors = 10

    for idx, item in enumerate(tqdm(dataset_iter, initial=start_idx, desc="Salvando audio")):
        actual_idx = start_idx + idx

        try:
            # Limita numero di sample se richiesto
            if max_samples and actual_idx >= max_samples:
                print(f"\n⏸️  Limite raggiunto: {max_samples} sample processati")
                break

            # Salva audio con retry
            audio_filename = f"LJ_{actual_idx:06d}.wav"
            audio_path = os.path.join(wavs_dir, audio_filename)

            def save_audio():
                audio_data = item['audio']
                sf.write(audio_path, audio_data['array'], audio_data['sampling_rate'])
                return audio_data

            try:
                retry_with_backoff(save_audio, max_retries=3, initial_wait=1, max_wait=10)
            except Exception as e:
                print(f"\n⚠️  Impossibile salvare {audio_filename}: {e}")
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    print(f"\n❌ Troppi errori consecutivi ({consecutive_errors}), interrompo...")
                    break
                continue

            # Reset errori consecutivi
            consecutive_errors = 0

            # Aggiungi a metadata
            text = item['text']
            metadata_lines.append(f"{audio_filename}|{text}")

            processed += 1

            # Salva checkpoint ogni 50 file
            if processed % 50 == 0:
                checkpoint_data = {
                    'processed': processed,
                    'metadata': metadata_lines
                }
                save_checkpoint(checkpoint_path, checkpoint_data)

                # Info RAM
                ram = psutil.virtual_memory()
                ram_used_gb = ram.used / (1024**3)
                print(f"\n💾 Checkpoint salvato | File: {processed} | RAM: {ram_used_gb:.1f}GB")

            # Libera memoria ogni 100 file
            if streaming and processed % 100 == 0:
                gc.collect()

        except StopIteration:
            print(f"\n✅ Fine dataset raggiunta")
            break
        except Exception as e:
            print(f"\n⚠️  Errore sample {actual_idx}: {e}")
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                print(f"\n❌ Troppi errori consecutivi, interrompo...")
                break
            continue

    # Salva metadata.csv finale
    metadata_path = os.path.join(output_dir, "metadata.csv")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(metadata_lines))

    print(f"\n✅ Completato!")
    print(f"   📊 {processed} file audio salvati")
    print(f"   📄 metadata.csv creato")
    print(f"   💾 Totale: ~{processed * 0.5:.1f} MB")

    # Rimuovi checkpoint se download completato con successo
    if os.path.exists(checkpoint_path):
        try:
            os.remove(checkpoint_path)
            print(f"   🧹 Checkpoint rimosso")
        except Exception as e:
            print(f"   ⚠️  Errore rimozione checkpoint: {e}")

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
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Non riprendere da checkpoint (riavvia download da zero)"
    )
    args = parser.parse_args()

    # Esegui download
    download_ljspeech_italian(
        output_dir=args.output_dir,
        dataset_name=args.dataset,
        max_samples=args.max_samples,
        streaming=not args.no_streaming,
        resume=not args.no_resume
    )
