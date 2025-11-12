"""
Converte audio usando scipy (non richiede ffmpeg)
"""
from scipy.io import wavfile
import numpy as np
import soundfile as sf

print("Tentativo conversione con scipy...")
print()

input_file = "Addestramento_Voce.wav"
output_file = "Addestramento_Voce_convertito.wav"

try:
    # Prova a leggere con scipy
    print(f"Lettura {input_file}...")
    sample_rate, data = wavfile.read(input_file)

    print(f"  Sample rate: {sample_rate}Hz")
    print(f"  Shape: {data.shape}")
    print(f"  Dtype: {data.dtype}")
    print()

    # Converti a mono se stereo
    if len(data.shape) > 1:
        print(f"Conversione a mono (da {data.shape[1]} canali)...")
        data = np.mean(data, axis=1)

    # Normalizza a float32 [-1, 1]
    print("Normalizzazione...")
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    else:
        data = data.astype(np.float32)

    # Resample se necessario (opzionale)
    target_sr = 22050
    if sample_rate != target_sr:
        print(f"Resampling {sample_rate}Hz -> {target_sr}Hz...")
        from scipy import signal
        num_samples = int(len(data) * target_sr / sample_rate)
        data = signal.resample(data, num_samples)
        sample_rate = target_sr

    # Salva con soundfile (formato standard)
    print(f"Salvataggio {output_file}...")
    sf.write(output_file, data, sample_rate, subtype='PCM_16')

    print()
    print("=" * 60)
    print("Conversione completata!")
    print(f"File: {output_file}")
    print("=" * 60)

    # Verifica
    print()
    print("Verifica file...")
    info = sf.info(output_file)
    print(f"  Sample rate: {info.samplerate}Hz")
    print(f"  Channels: {info.channels}")
    print(f"  Duration: {info.duration:.1f}s")
    print()
    print("OK! File pronto per XTTS")

except Exception as e:
    print(f"ERRORE: {e}")
    import traceback
    traceback.print_exc()
