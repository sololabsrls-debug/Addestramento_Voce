"""
Genera audio di 30 secondi sul problema affitti a Milano
usando la voce in Addestramento_Voce.wav
"""
import torch
import time
from TTS.api import TTS

print("=" * 60)
print("GENERAZIONE AUDIO - Affitti Milano")
print("=" * 60)
print()

# Audio di riferimento (convertito)
audio_ref = "Addestramento_Voce_convertito.wav"
print(f"Audio riferimento: {audio_ref}")
print()

# Testo sul problema affitti a Milano (~30 secondi di audio)
testo = """
Il mercato degli affitti a Milano è diventato una vera emergenza.
I prezzi sono aumentati del quaranta per cento negli ultimi cinque anni,
rendendo impossibile per molti giovani e famiglie trovare un alloggio
accessibile. Una stanza singola in zona semi-centrale può costare oltre
seicento euro al mese, mentre un bilocale supera facilmente i mille
cinquecento euro. Questa situazione spinge sempre più persone a lasciare
la città, con conseguenze negative per il tessuto sociale ed economico.
"""

print("Testo da sintetizzare:")
print("-" * 60)
print(testo.strip())
print("-" * 60)
print()

# Carica modello
print("Caricamento modello XTTS...")
start = time.time()
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=torch.cuda.is_available())
print(f"Modello caricato in {time.time() - start:.1f}s")
print()

# Genera audio
print("Sintesi in corso...")
output_file = "temp_test/affitti_milano.wav"
start = time.time()

tts.tts_to_file(
    text=testo,
    speaker_wav=audio_ref,
    file_path=output_file,
    language="it"
)

elapsed = time.time() - start
print(f"Completato in {elapsed:.1f}s")
print()

print("=" * 60)
print("RISULTATO:")
print(f"File: {output_file}")
print()
print("Ascoltalo per sentire la voce clonata parlare degli affitti!")
print("=" * 60)
