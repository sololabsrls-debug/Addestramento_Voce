# ⚡ Piper TTS - Quick Start (2 Passi)

## 🎯 Vuoi addestrare un modello TTS in 2 passi? Ecco come!

---

## 📋 Prima di Iniziare

**Hai bisogno di:**
- ✅ Account Google (per Colab)
- ✅ Dataset audio (min 30 min per fine-tuning, 2h per training)
- ✅ 8-16 ore di tempo (il training gira in background)

---

## 🚀 Passo 1: Scegli il Percorso

### Opzione A: Fine-Tuning (Veloce) ⚡

**Quando:** Hai 30-60 minuti di audio, vuoi risultati rapidi

**Tempo:** ~8-12 ore

**Notebook:** `Piper_FineTuning_Colab.ipynb`

```
👉 Apri → Piper_FineTuning_Colab.ipynb
👉 Clicca → "Open in Colab"
👉 Esegui tutte le celle (Runtime → Run all)
```

---

### Opzione B: Training Completo (Professionale) 🎯

**Quando:** Hai 2+ ore di audio, vuoi massima qualità

**Tempo:** ~12-16 ore

**Notebook:** `Piper_Training_Complete.ipynb`

```
👉 Apri → Piper_Training_Complete.ipynb
👉 Clicca → "Open in Colab"
👉 Esegui tutte le celle (Runtime → Run all)
```

---

## 📁 Passo 2: Prepara il Dataset

### Struttura Richiesta

```
my_dataset/
├── wavs/
│   ├── audio_001.wav   ← 22050Hz, mono, 16-bit
│   ├── audio_002.wav
│   └── ...
└── metadata.csv        ← filename|trascrizione
```

### Crea metadata.csv

**Formato:**
```
audio_001|Questa è la prima frase.
audio_002|Questa è la seconda frase.
audio_003|E così via per tutti i file.
```

**⚠️ IMPORTANTE:**
- ❌ NO header
- ❌ NO estensione .wav nel filename
- ✅ Separatore: `|` (pipe)

---

## ✅ Checklist Veloce

Prima di avviare il training:

- [ ] Ho 30+ minuti di audio (fine-tuning) o 2+ ore (training)
- [ ] Tutti i WAV sono 22050Hz, mono, 16-bit
- [ ] metadata.csv è formattato correttamente
- [ ] Ho verificato che almeno 3 file audio si caricano senza errori
- [ ] Ho attivato GPU su Colab (Runtime → Change runtime type → GPU)

---

## 🎬 Workflow Completo (3 Minuti)

### 1. Converti Audio (se necessario)

```bash
# Se hai MP3 o altri formati:
ffmpeg -i input.mp3 -ar 22050 -ac 1 output.wav
```

### 2. Carica su Google Drive

```
Google Drive/
└── my_piper_dataset/
    ├── wavs/
    └── metadata.csv
```

### 3. Apri Notebook Colab

- Vai su Google Colab
- Upload notebook (`Piper_FineTuning_Colab.ipynb` o `Piper_Training_Complete.ipynb`)
- Runtime → Change runtime type → GPU → Save

### 4. Modifica Percorso Dataset

Nel notebook, trova questa cella:
```python
DATASET_DIR = "/content/drive/MyDrive/my_dataset"  # ⚠️ MODIFICA QUI
```

Cambia con il tuo percorso Google Drive.

### 5. Run All

```
Runtime → Run all
```

Fatto! Vai a prendere un caffè (o 10). ☕

---

## 📊 Monitoraggio

### Durante il Training

```
[Epoch 1000/10000] Loss: 2.345
[Epoch 2000/10000] Loss: 1.876
[Epoch 3000/10000] Loss: 1.542
```

**Loss atteso:**
- Inizio: ~3.0-5.0
- Metà: ~1.5-2.0
- Fine: ~0.8-1.2

### Quanto Manca?

**Fine-tuning (8-12h):**
- 25% → 2-3h
- 50% → 4-6h
- 75% → 6-9h
- 100% → 8-12h

**Training completo (12-16h):**
- 25% → 3-4h
- 50% → 6-8h
- 75% → 9-12h
- 100% → 12-16h

---

## 🎵 Download Modello

Al termine, il notebook genererà:

```
✅ my_piper_model.zip
   ├── model.onnx       ← Modello TTS
   └── config.json      ← Configurazione
```

**Download automatico** alla fine del notebook!

---

## 🧪 Test Veloce

```bash
# Installa Piper
pip install piper-tts

# Testa modello
echo "Ciao, questo è un test" | piper \
    --model model.onnx \
    --output_file test.wav
```

---

## 🐛 Problemi Comuni

### "CUDA out of memory"

**Soluzione:** Nel notebook, trova:
```python
"batch_size": 16
```
Cambia in:
```python
"batch_size": 8
```

---

### "File not found: metadata.csv"

**Soluzione:** Verifica percorso Google Drive:
```python
DATASET_DIR = "/content/drive/MyDrive/NOME_CORRETTO_CARTELLA"
```

---

### Audio distorto

**Cause:**
1. WAV non è 22050Hz mono → Riconverti con ffmpeg
2. Training insufficiente → Continua per più epochs
3. Dataset rumoroso → Pulisci audio

---

### Training troppo lento

**Soluzione:** Verifica GPU sia attiva:
```python
!nvidia-smi
```

Se non vedi info GPU: Runtime → Change runtime type → GPU

---

## 📚 Approfondimenti

**Vuoi saperne di più?**

- 📖 Guida completa: `PIPER_TRAINING_GUIDE.md`
- 🔬 Configurazione avanzata: leggi config.json nel notebook
- 💬 Community: [Piper Discussions](https://github.com/rhasspy/piper/discussions)

---

## 🎯 TL;DR (Troppo Lungo, Non Ho Letto)

```bash
# 1. Prepara dataset
my_dataset/
├── wavs/*.wav          # 22050Hz mono
└── metadata.csv        # filename|text

# 2. Upload su Google Drive

# 3. Apri notebook Colab
- Piper_FineTuning_Colab.ipynb (veloce)
- Piper_Training_Complete.ipynb (completo)

# 4. Attiva GPU
Runtime → Change runtime type → GPU

# 5. Modifica percorso dataset
DATASET_DIR = "/content/drive/MyDrive/..."

# 6. Run all
Runtime → Run all

# 7. Aspetta 8-16h

# 8. Download my_piper_model.zip

# Fine! 🎉
```

---

**Buon training! 🚀**

Problemi? Leggi `PIPER_TRAINING_GUIDE.md` per troubleshooting dettagliato.
