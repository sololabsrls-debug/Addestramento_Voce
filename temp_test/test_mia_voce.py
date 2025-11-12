"""
Test voice cloning con la TUA voce
"""
import torch
import time
from TTS.api import TTS

print("=" * 60)
print("VOICE CLONING - Test con la tua voce")
print("=" * 60)
print()

# Carica modello (usa cache, sara' veloce)
print("Caricamento modello XTTS...")
start = time.time()
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=torch.cuda.is_available())
print(f"Caricato in {time.time() - start:.1f}s")
print()

# Audio di riferimento (la TUA voce)
audio_ref = "mia_voce_riferimento.wav"
print(f"Audio riferimento: {audio_ref} (la TUA voce registrata)")
print()

# Testo di test - Qualcosa che NON hai letto nella registrazione
testo = "Buongiorno, questo e' un test del sistema di voice cloning. Sto testando come suona la mia voce clonata con frasi che non ho mai pronunciato prima."

print("Testo da sintetizzare:")
print(f'"{testo}"')
print()

# Genera audio
print("Sintesi in corso...")
start = time.time()

tts.tts_to_file(
    text=testo,
    speaker_wav=audio_ref,
    file_path="temp_test/output_mia_voce_clonata.wav",
    language="it"
)

elapsed = time.time() - start
print(f"Completato in {elapsed:.1f}s")
print()

print("=" * 60)
print("RISULTATO:")
print("File: temp_test/output_mia_voce_clonata.wav")
print()
print("ASCOLTALO! Dovrebbe suonare come la TUA voce")
print("anche se stai dicendo frasi che non hai registrato!")
print("=" * 60)
