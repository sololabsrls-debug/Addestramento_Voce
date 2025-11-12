"""
Script per pulire la cartella temp_test
Cancella tutti i file audio generati dai test
"""
import os
import glob

temp_dir = "temp_test"

# Trova tutti i file audio
audio_files = glob.glob(f"{temp_dir}/*.wav") + glob.glob(f"{temp_dir}/*.mp3")

if not audio_files:
    print("Nessun file da cancellare in temp_test/")
else:
    print(f"Trovati {len(audio_files)} file da cancellare:")
    for f in audio_files:
        print(f"  - {f}")

    conferma = input("\nConfermi cancellazione? (s/n): ")

    if conferma.lower() == 's':
        for f in audio_files:
            os.remove(f)
            print(f"Cancellato: {f}")
        print(f"\n✓ Cartella temp_test/ pulita!")
    else:
        print("Operazione annullata")
