"""
Script per registrare la tua voce per voice cloning - VERSIONE AUTO
"""
import sounddevice as sd
import soundfile as sf
import time

print("=" * 60)
print("REGISTRAZIONE VOCE PER VOICE CLONING")
print("=" * 60)
print()

# Configurazione
SAMPLE_RATE = 48000  # Qualita' alta
DURATION = 15  # 15 secondi
OUTPUT_FILE = "mia_voce_riferimento.wav"

print("TESTO DA LEGGERE:")
print("-" * 60)
print("Ciao, mi chiamo [il tuo nome]. Questa registrazione viene")
print("usata per clonare la mia voce. Sto parlando in modo naturale")
print("e chiaro. La tecnologia di voice cloning e' davvero")
print("interessante. Buona giornata!")
print("-" * 60)
print()

# Countdown
for i in range(3, 0, -1):
    print(f"Inizia tra {i}...")
    time.sleep(1)

print()
print("REGISTRAZIONE IN CORSO... ({} secondi)".format(DURATION))
print("Leggi il testo sopra ad alta voce!")
print()

# Registra
audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,  # Mono
    dtype='float32'
)

# Mostra progresso
for i in range(DURATION):
    time.sleep(1)
    print(f"  {i+1}/{DURATION} secondi...")

sd.wait()  # Aspetta fine registrazione

print()
print("Registrazione completata!")
print()

# Salva file
sf.write(OUTPUT_FILE, audio, SAMPLE_RATE)

print(f"File salvato: {OUTPUT_FILE}")
print()
print("=" * 60)
