# 🔍 Script di Verifica Dataset

## Descrizione

Script Python per verificare che il dataset sia nel formato corretto per l'addestramento TTS con Coqui o Piper.

**✓ NON RICHIEDE GPU** - Può essere eseguito ovunque (locale, Colab CPU, ecc.)

## Cosa verifica

### 1. File WAV
- ✓ Sample rate: 22050 Hz o 16000 Hz
- ✓ Canali: 1 (mono)
- ✓ Bit depth: 16-bit
- ✓ Durata: 1-10 secondi (ideale 3-7s)
- ✓ Formato WAV valido

### 2. File metadata.csv
- ✓ Formato corretto: `wavs/filename.wav|Testo trascrizione`
- ✓ Tutti i file WAV referenziati esistono
- ✓ Nessun testo vuoto
- ✓ Lunghezza testo appropriata (10-200 caratteri)

### 3. Struttura Directory
```
dataset/
├── wavs/
│   ├── audio1.wav
│   ├── audio2.wav
│   └── ...
└── metadata.csv
```

## Come usare

### Opzione 1: Con percorso
```bash
python verify_dataset.py /percorso/al/dataset
```

### Opzione 2: Interattivo
```bash
python verify_dataset.py
# Ti chiederà il percorso (default: ./dataset)
```

### Opzione 3: Directory corrente
```bash
cd /percorso/al/dataset/..
python verify_dataset.py ./dataset
```

## Esempio Output

```
=== VERIFICA DATASET TTS ===

Directory dataset: /home/user/dataset

[1] Verifica struttura directory
✓ Directory wavs trovata: /home/user/dataset/wavs

[2] Verifica metadata.csv
✓ File metadata.csv trovato
✓ Righe valide: 150

[3] Verifica file WAV
ℹ Trovati 150 file WAV

Analisi file WAV:
✓ audio_001.wav: Formato perfetto: 22050Hz, mono, 16bit, 4.5s
✓ audio_002.wav: Formato perfetto: 22050Hz, mono, 16bit, 5.2s
⚠ audio_003.wav: Durata ok ma non ideale: 2.8s (ideale 3-7s)
...

=== RIEPILOGO ===

File WAV totali: 150
  ✓ Validi: 145
  ⚠ Con warning: 5

Durata totale audio: 12.5 minuti (750.0s)
Durata media: 5.0s per file

Sample rate:
  - 22050Hz: 150 file

Righe valide in metadata.csv: 150

=== RACCOMANDAZIONI ===

ℹ Dataset sufficiente (12.5min). Per risultati ottimali considera 1-2 ore di audio

=== VERDETTO FINALE ===

✓ Dataset pronto per l'addestramento!
```

## Su Google Colab

### 1. Carica lo script
```python
# In una cella Colab
!wget https://raw.githubusercontent.com/tuouser/tuorepo/main/verify_dataset.py
```

Oppure caricalo manualmente:
```python
# Carica verify_dataset.py usando il file browser di Colab
```

### 2. Esegui senza GPU
```python
# Cambia runtime in CPU se necessario
# Runtime > Change runtime type > Hardware accelerator > None

!python verify_dataset.py /content/dataset
```

## Codici di uscita

- `0`: Dataset valido (con o senza warning)
- `1`: Dataset con errori critici

## Troubleshooting

### "Directory non trovata"
- Verifica che il percorso sia corretto
- Usa percorsi assoluti se hai dubbi

### "Nessun file WAV trovato"
- Controlla che i file siano nella sottodirectory `wavs/`
- Verifica che abbiano estensione `.wav` (minuscolo)

### "Sample rate errato"
Converti i file con ffmpeg:
```bash
ffmpeg -i input.wav -ar 22050 -ac 1 -sample_fmt s16 output.wav
```

### "File non trovato" nel metadata.csv
- Verifica che il percorso in metadata.csv sia: `wavs/filename.wav`
- NON usare percorsi assoluti o `./wavs/filename.wav`

## Prossimi passi

Una volta che lo script dice **"✓ Dataset pronto per l'addestramento!"**:

1. ✓ Il dataset è pronto
2. Aspetta che la GPU di Colab si resetti
3. Avvia il notebook di training:
   - `piper_training/Piper_Training_Complete.ipynb`
   - Oppure `piper_training/Piper_FineTuning_Colab.ipynb`

## Requisiti

```bash
pip install wave  # Già incluso in Python standard library
```

Nessuna altra dipendenza richiesta!
