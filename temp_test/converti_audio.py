"""
Converte Addestramento_Voce.wav in formato compatibile con XTTS
"""
from pydub import AudioSegment
import soundfile as sf
import numpy as np

print("Conversione audio in formato compatibile...")
print()

input_file = "Addestramento_Voce.wav"
output_file = "Addestramento_Voce_convertito.wav"

try:
    # Carica con pydub (supporta molti formati)
    print(f"Caricamento {input_file}...")
    audio = AudioSegment.from_file(input_file)

    print(f"  Sample rate: {audio.frame_rate}Hz")
    print(f"  Channels: {audio.channels}")
    print(f"  Duration: {len(audio)/1000:.1f}s")
    print()

    # Converti a mono se stereo
    if audio.channels > 1:
        print("Conversione a mono...")
        audio = audio.set_channels(1)

    # Imposta sample rate a 22050 o 48000 (ottimale per XTTS)
    target_sr = 22050
    if audio.frame_rate != target_sr:
        print(f"Resampling a {target_sr}Hz...")
        audio = audio.set_frame_rate(target_sr)

    # Esporta come WAV standard (PCM 16-bit)
    print(f"Salvataggio {output_file}...")
    audio.export(output_file, format="wav")

    print()
    print("=" * 60)
    print(f"Conversione completata!")
    print(f"File convertito: {output_file}")
    print("=" * 60)

    # Verifica che sia leggibile
    print()
    print("Verifica file convertito...")
    info = sf.info(output_file)
    print(f"  Sample rate: {info.samplerate}Hz")
    print(f"  Channels: {info.channels}")
    print(f"  Duration: {info.duration:.1f}s")
    print(f"  Format: {info.format}")
    print()
    print("OK! File pronto per XTTS")

except Exception as e:
    print(f"ERRORE: {e}")
    print()
    print("Il file potrebbe essere corrotto o in un formato non supportato.")
