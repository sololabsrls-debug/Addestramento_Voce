# 📚 Piper TTS Training - Guida Completa

## 📋 Indice
- [Introduzione](#introduzione)
- [Requisiti](#requisiti)
- [Preparazione Dataset](#preparazione-dataset)
- [Training vs Fine-Tuning](#training-vs-fine-tuning)
- [Configurazione Training](#configurazione-training)
- [Processo di Training](#processo-di-training)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [FAQ](#faq)

---

## 🎯 Introduzione

Piper è un TTS (Text-to-Speech) veloce e locale basato su VITS (Variational Inference with adversarial learning for end-to-end Text-to-Speech).

**Vantaggi:**
- ✅ Completamente offline
- ✅ Veloce (real-time su CPU)
- ✅ Qualità eccellente
- ✅ Multi-lingua
- ✅ Open source

**Quando usare Training vs Fine-Tuning:**

| Caratteristica | Training da Zero | Fine-Tuning |
|---------------|------------------|-------------|
| Dataset minimo | 2+ ore | 30+ minuti |
| Tempo training | 12-16 ore | 8-12 ore |
| Controllo | Massimo | Medio |
| Difficoltà | Alta | Media |
| Caso d'uso | Nuove lingue/accenti | Adattare voce esistente |

---

## 💻 Requisiti

### Hardware
- **GPU:** NVIDIA con almeno 8GB VRAM (consigliato: T4, V100, A100)
- **RAM:** 16GB+ consigliati
- **Storage:** 10GB+ liberi

### Software
- Python 3.8+
- CUDA 11.x o superiore
- Git

### Google Colab
- Account Google
- Colab Pro consigliato per training lunghi (evita disconnessioni)

---

## 📁 Preparazione Dataset

### Struttura Richiesta

```
my_dataset/
├── wavs/              # File audio WAV
│   ├── audio_001.wav
│   ├── audio_002.wav
│   └── ...
└── metadata.csv       # Trascrizioni
```

### Requisiti Audio

**Formato:**
- **Sample rate:** 22050 Hz (consigliato) o 16000 Hz
- **Bit depth:** 16-bit
- **Canali:** Mono
- **Formato:** WAV non compresso

**Conversione con ffmpeg:**
```bash
# Converti singolo file
ffmpeg -i input.mp3 -ar 22050 -ac 1 -c:a pcm_s16le output.wav

# Batch conversion (tutti i file in una cartella)
for file in *.mp3; do
    ffmpeg -i "$file" -ar 22050 -ac 1 -c:a pcm_s16le "wavs/${file%.mp3}.wav"
done
```

### Formato metadata.csv

**Struttura:** `filename|trascrizione`

**Esempio:**
```
audio_001|Questa è la prima frase di esempio.
audio_002|La qualità del dataset determina la qualità del modello.
audio_003|Ogni frase deve essere trascritta accuratamente.
```

**IMPORTANTE:**
- ❌ NO header nel file
- ❌ NO estensione .wav nel filename
- ✅ Separatore: pipe `|`
- ✅ Trascrizioni accurate (no errori di battitura)
- ✅ Punteggiatura corretta

### Qualità Dataset

**Requisiti essenziali:**
- ✅ Audio pulito (no rumore di fondo)
- ✅ Volume consistente tra i file
- ✅ Singolo speaker per modello
- ✅ Trascrizioni precise (100% match con audio)

**Dimensione dataset:**

| Durata | Qualità Risultato | Note |
|--------|------------------|------|
| < 30 min | Scarsa | Training possibile ma risultati limitati |
| 30 min - 1 ora | Accettabile | Fine-tuning OK |
| 1-2 ore | Buona | Training da zero OK |
| 2-5 ore | Ottima | Qualità professionale |
| 5+ ore | Eccellente | Massima qualità |

### Tools per Preparazione Dataset

**LJSpeech-style dataset:**
```python
# Script per creare metadata.csv da cartella audio
import os
import glob

audio_files = sorted(glob.glob("wavs/*.wav"))
with open("metadata.csv", "w") as f:
    for audio_path in audio_files:
        filename = os.path.basename(audio_path).replace(".wav", "")
        # ⚠️ Inserisci trascrizione manuale o da ASR
        transcription = "TRASCRIZIONE QUI"
        f.write(f"{filename}|{transcription}\n")
```

**Trascrizione automatica (ASR):**
```python
# Usa Whisper per trascrizioni automatiche
import whisper

model = whisper.load_model("base")

for audio_file in glob.glob("wavs/*.wav"):
    result = model.transcribe(audio_file)
    print(f"{audio_file}: {result['text']}")
```

---

## 🎛️ Training vs Fine-Tuning

### Training da Zero

**Quando usarlo:**
- Lingua/accento non supportato
- Vuoi massimo controllo
- Hai 2+ ore di audio

**Pro:**
- Controllo totale su architettura
- Ottimizzato per il tuo dataset
- Nessuna dipendenza da modelli pre-esistenti

**Contro:**
- Richiede più dati
- Training più lungo
- Più complesso da configurare

**Notebook:** `Piper_Training_Complete.ipynb`

---

### Fine-Tuning

**Quando usarlo:**
- Vuoi adattare voce esistente
- Hai 30-60 minuti di audio
- Vuoi risultati più rapidi

**Pro:**
- Richiede meno dati
- Training più veloce
- Setup più semplice

**Contro:**
- Limitato dalla base del modello pre-addestrato
- Meno flessibilità

**Notebook:** `Piper_FineTuning_Colab.ipynb`

---

## ⚙️ Configurazione Training

### File config.json

```json
{
  "audio": {
    "sample_rate": 22050,
    "max_wav_value": 32767.0,
    "filter_length": 1024,
    "hop_length": 256,
    "win_length": 1024
  },
  "model": {
    "name": "vits",
    "hidden_channels": 192,
    "inter_channels": 192,
    "filter_channels": 768,
    "n_heads": 2,
    "n_layers": 6,
    "kernel_size": 3,
    "p_dropout": 0.1
  },
  "training": {
    "epochs": 10000,
    "learning_rate": 0.0002,
    "batch_size": 16,
    "log_interval": 100,
    "save_interval": 1000,
    "num_workers": 4
  }
}
```

### Hyperparameters Spiegati

**Audio:**
- `sample_rate`: 22050 Hz (standard) o 16000 Hz (più veloce)
- `hop_length`: 256 (default, non modificare)

**Model:**
- `hidden_channels`: 192 (più alto = più qualità ma più lento)
- `n_layers`: 6 (più layer = modello più espressivo)
- `p_dropout`: 0.1 (previene overfitting)

**Training:**
- `epochs`: 10000 (training si ferma automaticamente quando converge)
- `learning_rate`: 0.0002 (0.0001-0.0003 è range sicuro)
- `batch_size`: 16 (riduci se OOM, aumenta se GPU potente)

### Tuning per GPU

| GPU | Batch Size | Note |
|-----|-----------|------|
| T4 (16GB) | 16 | Default Colab |
| V100 (32GB) | 32 | Raddoppia velocità |
| A100 (40GB) | 64 | Massima velocità |
| < 12GB | 8 | Riduci se OOM |

---

## 🚀 Processo di Training

### 1. Preprocessing

```bash
python piper_train/preprocess.py \
    --input-dir /path/to/dataset \
    --output-dir /path/to/output \
    --language it-it \
    --sample-rate 22050
```

**Output:**
- Genera file `.npy` per ogni audio (mel-spectrograms)
- Crea phoneme vocabulary
- Valida il dataset

**Tempo:** 5-10 minuti per 1h di audio

---

### 2. Training

```bash
python -m piper_train \
    --dataset-dir /path/to/preprocessed \
    --output-dir /path/to/checkpoints \
    --config config.json \
    --restore-checkpoint  # Riprende da ultimo checkpoint
```

**Cosa succede:**
1. Carica dataset preprocessato
2. Inizializza modello VITS
3. Training loop:
   - Forward pass
   - Calcola loss (reconstruction + adversarial)
   - Backward pass
   - Update weights
4. Salva checkpoint ogni N steps

**Monitoraggio:**
```
[Epoch 1000/10000] Loss: 2.345 | Duration: 1.23s/batch
[Epoch 2000/10000] Loss: 1.876 | Duration: 1.21s/batch
[Epoch 3000/10000] Loss: 1.542 | Duration: 1.19s/batch
```

**Loss atteso:**
- Inizio: ~3.0-5.0
- Dopo 2000 epochs: ~1.5-2.0
- Fine training: ~0.8-1.2

---

### 3. Export ONNX

```bash
python -m piper_train.export_onnx \
    checkpoints/checkpoint_10000.pt \
    model.onnx
```

**Output:**
- `model.onnx`: Modello pronto per inferenza
- `model.onnx.json`: Configurazione

**Dimensione file:** ~10-50MB a seconda della configurazione

---

## 🐛 Troubleshooting

### OOM (Out of Memory)

**Sintomo:**
```
RuntimeError: CUDA out of memory
```

**Soluzioni:**
1. **Riduci batch_size:**
   ```json
   "batch_size": 8  // invece di 16
   ```

2. **Riduci model complexity:**
   ```json
   "hidden_channels": 128,  // invece di 192
   "n_layers": 4           // invece di 6
   ```

3. **Usa GPU più potente:** Colab Pro con A100

---

### Audio Distorto

**Sintomo:** Output audio è metallico, distorto, o incomprensibile

**Cause comuni:**
1. **Sample rate errato:**
   - Verifica tutti WAV siano 22050Hz
   ```bash
   soxi wavs/*.wav | grep "Sample Rate"
   ```

2. **Dataset rumoroso:**
   - Pulisci audio con noise reduction
   - Rimuovi file con troppo rumore di fondo

3. **Training insufficiente:**
   - Continua training per più epochs
   - Verifica loss sia < 1.5

---

### Training Troppo Lento

**Sintomo:** < 0.5 batch/sec

**Soluzioni:**
1. **Verifica GPU:**
   ```python
   !nvidia-smi
   ```
   Deve mostrare utilizzo GPU ~90-100%

2. **Aumenta num_workers:**
   ```json
   "num_workers": 8  // invece di 4
   ```

3. **Usa sample_rate più basso:**
   ```json
   "sample_rate": 16000  // invece di 22050
   ```

---

### Loss Non Converge

**Sintomo:** Loss rimane > 2.0 dopo 5000 epochs

**Cause:**
1. **Learning rate troppo alto/basso:**
   - Prova: 0.0001, 0.0002, 0.0003

2. **Dataset problematico:**
   - Verifica metadata.csv (no errori)
   - Controlla audio (no silenzi lunghi)

3. **Config errata:**
   - Usa config di default
   - Non modificare parametri audio

---

### Checkpoint Corrotti

**Sintomo:**
```
Error loading checkpoint
```

**Soluzione:**
- Usa checkpoint precedente:
  ```bash
  python -m piper_train \
      --restore-checkpoint checkpoints/checkpoint_9000.pt
  ```

---

## ✅ Best Practices

### Dataset
- ✅ 1 speaker per modello
- ✅ Audio consistente (stesso microfono, ambiente)
- ✅ Trascrizioni 100% accurate
- ✅ Frasi varie (domande, esclamazioni, affermazioni)
- ❌ NO rumore di fondo
- ❌ NO silenzios lunghi (>2s)
- ❌ NO audio troppo corti (<1s)

### Training
- ✅ Monitora loss regolarmente
- ✅ Salva checkpoint ogni 1000 epochs
- ✅ Testa qualità ogni 2000 epochs
- ✅ Usa Colab Pro per training lunghi
- ❌ NO interruzioni frequenti
- ❌ NO modifiche config durante training

### Testing
- ✅ Testa con frasi DIVERSE dal training
- ✅ Varia lunghezza frasi (corte, medie, lunghe)
- ✅ Testa punteggiatura (!, ?, .)
- ✅ Chiedi feedback a terzi

---

## ❓ FAQ

### Q: Quanto dataset serve davvero?
**A:** Dipende:
- Fine-tuning: 30-60 min OK
- Training da zero: 2+ ore consigliato
- Qualità professionale: 5+ ore

---

### Q: Posso usare dataset multi-speaker?
**A:** No, 1 speaker per modello. Se hai multi-speaker:
1. Separa audio per speaker
2. Addestra 1 modello per speaker

---

### Q: Come miglioro qualità audio?
**A:**
1. Usa microfono decente (no laptop mic)
2. Registra in ambiente silenzioso
3. Normalizza volume
4. Rimuovi rumore con Audacity/RX

---

### Q: Training si è interrotto, cosa faccio?
**A:** Riprendi da ultimo checkpoint:
```bash
python -m piper_train \
    --restore-checkpoint  # Auto-trova ultimo checkpoint
```

---

### Q: Posso usare GPU locale invece di Colab?
**A:** Sì! Setup:
```bash
git clone https://github.com/rhasspy/piper
cd piper/src/python
pip install -e .
# Poi segui stessi passi del notebook
```

---

### Q: Come confronto qualità tra checkpoint?
**A:**
```python
# Test ogni checkpoint
for ckpt in checkpoints/*.pt:
    export_onnx(ckpt, f"models/test_{ckpt}.onnx")
    generate_sample(f"models/test_{ckpt}.onnx", "Frase di test")
    # Ascolta e confronta
```

---

### Q: Loss è basso ma audio è brutto, perché?
**A:** Loss basso ≠ qualità alta. Cause:
1. Overfitting: modello "memorizza" invece di "imparare"
   - Soluzione: Aumenta dataset
2. Dataset problematico (es. rumore)
   - Soluzione: Pulisci dataset
3. Config errata
   - Soluzione: Usa config di default

---

## 📚 Risorse

### Documentazione
- [Piper GitHub](https://github.com/rhasspy/piper)
- [VITS Paper](https://arxiv.org/abs/2106.06103)
- [Piper Training Guide (EN)](https://github.com/rhasspy/piper/blob/master/TRAINING.md)

### Community
- [Piper Discussions](https://github.com/rhasspy/piper/discussions)
- [Home Assistant Forum](https://community.home-assistant.io/)

### Tools
- [Audacity](https://www.audacityteam.org/) - Audio editing
- [Whisper](https://github.com/openai/whisper) - Trascrizione automatica
- [FFmpeg](https://ffmpeg.org/) - Conversione audio

---

## 🎯 Prossimi Passi

Dopo aver completato il training:

1. **Test approfondito:**
   - Prova 20+ frasi diverse
   - Varia punteggiatura e intonazione
   - Chiedi feedback

2. **Ottimizzazione:**
   - Se non sei soddisfatto, aumenta dataset
   - Prova diversi learning rates
   - Continua training per più epochs

3. **Deploy:**
   - Integra in applicazione
   - Usa `piper` CLI per inferenza
   - Considera export per mobile (TFLite)

4. **Condivisione:**
   - Pubblica modello (se open dataset)
   - Contribuisci a Piper community
   - Documenta processo

---

**Buon training! 🚀**

Per domande: apri issue su [Piper GitHub](https://github.com/rhasspy/piper/issues)
