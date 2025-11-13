#!/usr/bin/env python3
"""
Script di verifica dataset per Coqui TTS / Piper
Verifica formato WAV, metadata.csv e struttura directory
NON RICHIEDE GPU - può essere eseguito ovunque
"""

import os
import csv
import wave
import sys
from pathlib import Path
from typing import List, Tuple, Dict

class Colors:
    """Colori per output terminale"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def verify_wav_file(wav_path: str) -> Tuple[bool, str, Dict]:
    """
    Verifica che un file WAV sia valido per TTS

    Requisiti Coqui TTS / Piper:
    - Sample rate: 22050 Hz (consigliato) o 16000 Hz
    - Canali: 1 (mono)
    - Bit depth: 16-bit
    - Durata: 1-10 secondi (ideale 3-7 secondi)
    """
    try:
        with wave.open(wav_path, 'rb') as wav:
            params = wav.getparams()
            channels = params.nchannels
            sample_rate = params.framerate
            sample_width = params.sampwidth
            n_frames = params.nframes
            duration = n_frames / float(sample_rate)

            info = {
                'channels': channels,
                'sample_rate': sample_rate,
                'bit_depth': sample_width * 8,
                'duration': duration,
                'frames': n_frames
            }

            # Verifica canali (deve essere mono)
            if channels != 1:
                return False, f"Canali errati: {channels} (deve essere 1/mono)", info

            # Verifica sample rate
            if sample_rate not in [16000, 22050]:
                return False, f"Sample rate: {sample_rate}Hz (consigliato 22050Hz o 16000Hz)", info

            # Verifica bit depth
            if sample_width != 2:  # 2 bytes = 16 bit
                return False, f"Bit depth: {sample_width*8}bit (deve essere 16bit)", info

            # Verifica durata
            if duration < 1.0:
                return False, f"Troppo corto: {duration:.2f}s (minimo 1s)", info
            elif duration > 10.0:
                return False, f"Troppo lungo: {duration:.2f}s (massimo 10s)", info
            elif duration < 3.0 or duration > 7.0:
                return True, f"Durata ok ma non ideale: {duration:.2f}s (ideale 3-7s)", info

            return True, f"Formato perfetto: {sample_rate}Hz, mono, 16bit, {duration:.2f}s", info

    except Exception as e:
        return False, f"Errore lettura file: {str(e)}", {}

def verify_metadata_csv(csv_path: str, wavs_dir: str) -> Tuple[bool, List[str], int]:
    """
    Verifica il file metadata.csv

    Formato atteso:
    wavs/filename.wav|Testo della trascrizione
    """
    errors = []
    valid_lines = 0

    if not os.path.exists(csv_path):
        return False, [f"File non trovato: {csv_path}"], 0

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) == 0:
            return False, ["File metadata.csv vuoto"], 0

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                errors.append(f"Riga {i}: riga vuota")
                continue

            # Verifica formato pipe-separated
            if '|' not in line:
                errors.append(f"Riga {i}: manca separatore '|'")
                continue

            parts = line.split('|')
            if len(parts) != 2:
                errors.append(f"Riga {i}: formato errato (atteso: filename.wav|testo)")
                continue

            wav_file, text = parts

            # Verifica che il file WAV esista
            wav_path = os.path.join(wavs_dir, os.path.basename(wav_file))
            if not os.path.exists(wav_path):
                errors.append(f"Riga {i}: file non trovato: {wav_file}")
                continue

            # Verifica che il testo non sia vuoto
            if not text.strip():
                errors.append(f"Riga {i}: testo vuoto per {wav_file}")
                continue

            # Verifica lunghezza testo (ideale: 10-150 caratteri)
            text_len = len(text.strip())
            if text_len < 10:
                errors.append(f"Riga {i}: testo troppo corto ({text_len} caratteri)")
            elif text_len > 200:
                errors.append(f"Riga {i}: testo troppo lungo ({text_len} caratteri)")

            valid_lines += 1

        return len(errors) == 0, errors, valid_lines

    except Exception as e:
        return False, [f"Errore lettura CSV: {str(e)}"], 0

def main():
    print(f"\n{Colors.BOLD}=== VERIFICA DATASET TTS ==={Colors.END}\n")

    # Chiedi la directory del dataset
    if len(sys.argv) > 1:
        dataset_dir = sys.argv[1]
    else:
        dataset_dir = input("Inserisci il percorso della directory del dataset [./dataset]: ").strip()
        if not dataset_dir:
            dataset_dir = "./dataset"

    dataset_path = Path(dataset_dir)

    if not dataset_path.exists():
        print_error(f"Directory non trovata: {dataset_dir}")
        print_info("Crea la directory con questa struttura:")
        print("  dataset/")
        print("  ├── wavs/")
        print("  │   ├── file1.wav")
        print("  │   └── file2.wav")
        print("  └── metadata.csv")
        return 1

    # Verifica struttura directory
    print_info(f"Directory dataset: {dataset_path.absolute()}\n")

    wavs_dir = dataset_path / "wavs"
    metadata_file = dataset_path / "metadata.csv"

    # 1. Verifica esistenza directory wavs
    print(f"{Colors.BOLD}[1] Verifica struttura directory{Colors.END}")
    if not wavs_dir.exists():
        print_error(f"Directory 'wavs' non trovata in {dataset_path}")
        return 1
    print_success(f"Directory wavs trovata: {wavs_dir}")

    # 2. Verifica esistenza metadata.csv
    print(f"\n{Colors.BOLD}[2] Verifica metadata.csv{Colors.END}")
    if not metadata_file.exists():
        print_error(f"File metadata.csv non trovato in {dataset_path}")
        return 1
    print_success(f"File metadata.csv trovato")

    # 3. Verifica contenuto metadata.csv
    is_valid, errors, valid_lines = verify_metadata_csv(str(metadata_file), str(wavs_dir))

    if errors:
        print_warning(f"Trovati {len(errors)} problemi in metadata.csv:")
        for error in errors[:10]:  # Mostra solo i primi 10 errori
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... e altri {len(errors)-10} errori")

    if valid_lines > 0:
        print_success(f"Righe valide: {valid_lines}")
    else:
        print_error("Nessuna riga valida trovata in metadata.csv")
        return 1

    # 4. Verifica file WAV
    print(f"\n{Colors.BOLD}[3] Verifica file WAV{Colors.END}")
    wav_files = list(wavs_dir.glob("*.wav"))

    if not wav_files:
        print_error("Nessun file WAV trovato nella directory wavs/")
        return 1

    print_info(f"Trovati {len(wav_files)} file WAV")

    valid_wavs = 0
    warning_wavs = 0
    error_wavs = 0

    total_duration = 0.0
    sample_rates = {}

    print("\nAnalisi file WAV:")
    for wav_file in wav_files:
        is_valid, msg, info = verify_wav_file(str(wav_file))

        if is_valid:
            if "ideale" in msg:
                print_warning(f"  {wav_file.name}: {msg}")
                warning_wavs += 1
            else:
                print_success(f"  {wav_file.name}: {msg}")
                valid_wavs += 1

            if info:
                total_duration += info.get('duration', 0)
                sr = info.get('sample_rate', 0)
                sample_rates[sr] = sample_rates.get(sr, 0) + 1
        else:
            print_error(f"  {wav_file.name}: {msg}")
            error_wavs += 1

    # 5. Riepilogo finale
    print(f"\n{Colors.BOLD}=== RIEPILOGO ==={Colors.END}\n")

    print(f"File WAV totali: {len(wav_files)}")
    print(f"  {Colors.GREEN}✓ Validi: {valid_wavs}{Colors.END}")
    if warning_wavs > 0:
        print(f"  {Colors.YELLOW}⚠ Con warning: {warning_wavs}{Colors.END}")
    if error_wavs > 0:
        print(f"  {Colors.RED}✗ Con errori: {error_wavs}{Colors.END}")

    print(f"\nDurata totale audio: {total_duration/60:.1f} minuti ({total_duration:.1f}s)")
    print(f"Durata media: {total_duration/len(wav_files):.1f}s per file")

    if sample_rates:
        print("\nSample rate:")
        for sr, count in sorted(sample_rates.items()):
            print(f"  - {sr}Hz: {count} file")

    print(f"\nRighe valide in metadata.csv: {valid_lines}")

    # Raccomandazioni
    print(f"\n{Colors.BOLD}=== RACCOMANDAZIONI ==={Colors.END}\n")

    if total_duration < 600:  # 10 minuti
        print_warning(f"Dataset piccolo ({total_duration/60:.1f}min). Per risultati migliori serve almeno 30-60 minuti di audio")
    elif total_duration < 1800:  # 30 minuti
        print_info(f"Dataset sufficiente ({total_duration/60:.1f}min). Per risultati ottimali considera 1-2 ore di audio")
    else:
        print_success(f"Dataset di buone dimensioni ({total_duration/60:.1f}min)")

    if error_wavs > 0:
        print_warning("Correggi i file WAV con errori prima dell'addestramento")

    if len(errors) > 0:
        print_warning("Correggi gli errori in metadata.csv prima dell'addestramento")

    # Verdict finale
    print(f"\n{Colors.BOLD}=== VERDETTO FINALE ==={Colors.END}\n")

    if error_wavs == 0 and len(errors) == 0 and valid_lines > 0:
        print_success("✓ Dataset pronto per l'addestramento!")
        return 0
    elif error_wavs > len(wav_files) * 0.5:  # Più del 50% errori
        print_error("✗ Dataset non pronto: troppi errori nei file WAV")
        return 1
    elif len(errors) > valid_lines * 0.5:  # Più del 50% errori
        print_error("✗ Dataset non pronto: troppi errori in metadata.csv")
        return 1
    else:
        print_warning("⚠ Dataset utilizzabile ma con alcuni problemi da correggere")
        return 0

if __name__ == "__main__":
    sys.exit(main())
