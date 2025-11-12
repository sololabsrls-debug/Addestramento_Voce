# 📊 Dataset Italiani per TTS Training

Questa guida elenca i dataset disponibili per training di modelli TTS in italiano.

## 🎤 Dataset LJSpeech-Italian

### Dataset Disponibili su Hugging Face:

#### 1. z-uo/female-LJSpeech-italian ⭐ CONSIGLIATO
- **Voce**: Femminile
- **Durata**: 8h 23m
- **Speaker**: 1 (voce singola)
- **Sample Rate**: 16kHz
- **Dimensione**: ~600 MB
- **Fonte**: M-AILABS Speech Dataset
- **Uso ideale**: Call center, assistenti vocali, applicazioni commerciali
- **Link**: https://huggingface.co/datasets/z-uo/female-LJSpeech-italian

```python
from datasets import load_dataset
dataset = load_dataset("z-uo/female-LJSpeech-italian", split="train")
```

#### 2. z-uo/male-LJSpeech-italian
- **Voce**: Maschile
- **Durata**: 31h 45m
- **Speaker**: 1 (voce singola)
- **Sample Rate**: 16kHz
- **Dimensione**: ~2.5 GB
- **Fonte**: M-AILABS Speech Dataset
- **Uso ideale**: Training esteso, alta qualità
- **Link**: https://huggingface.co/datasets/z-uo/male-LJSpeech-italian

```python
from datasets import load_dataset
dataset = load_dataset("z-uo/male-LJSpeech-italian", split="train")
```

---

## 🗂️ Altri Dataset Italiani Disponibili

### Common Voice

#### sarulab-speech/commonvoice22_sidon
- **Tipo**: Multi-speaker
- **Lingua**: Italiano (e altre)
- **Variabilità**: Alta (molti speaker diversi)
- **Uso**: Training robusto multi-speaker

### LibriSpeech

#### facebook/multilingual_librispeech
- **Tipo**: Multi-speaker
- **Lingue**: Multiple (include italiano)
- **Qualità**: Alta
- **Uso**: Training multi-lingue

### Dataset Specializzati

#### giacomoarienti/female-LJSpeech-italian
- **Nota**: Potrebbe essere rinominato o non più disponibile
- **Alternativa**: Usa `z-uo/female-LJSpeech-italian`

#### None1145/Vulpisfoglia
- **Tipo**: Dataset specifico italiano
- **Verifica disponibilità** prima dell'uso

---

## 📥 Come Scaricare e Usare

### Metodo 1: Script Python (Locale)

```bash
python scripts/download_ljspeech_italian.py \
  --dataset z-uo/female-LJSpeech-italian \
  --output-dir ./dataset/ljspeech_italian
```

**Opzioni disponibili**:
- `--dataset`: Scegli tra `z-uo/female-LJSpeech-italian` o `z-uo/male-LJSpeech-italian`
- `--output-dir`: Percorso di destinazione

### Metodo 2: Google Colab Notebook

1. Apri `Colab_FineTuning/Piper_Dataset_Preparation.ipynb`
2. Carica su Google Colab
3. Scegli dataset (female/male) nella cella
4. Esegui tutte le celle

### Metodo 3: Codice Python Diretto

```python
from datasets import load_dataset
import soundfile as sf
import os

# Scarica dataset
dataset = load_dataset("z-uo/female-LJSpeech-italian", split="train")

# Salva audio
for idx, item in enumerate(dataset):
    audio_data = item['audio']
    text = item['text']

    # Salva file audio
    sf.write(f"audio_{idx:06d}.wav",
             audio_data['array'],
             audio_data['sampling_rate'])

    print(f"{idx}: {text}")
```

---

## 🔧 Troubleshooting

### Errore: `ImportError: To support decoding audio data, please install 'torchcodec'`

**Soluzione**:
```bash
pip install torchcodec
```

Oppure usa il codice auto-installante:
```python
try:
    import torchcodec
except ImportError:
    !pip install -q torchcodec
```

### Errore: `DatasetNotFoundError: Dataset '...' doesn't exist`

**Causa**: Nome dataset errato

**Verifica nomi corretti**:
- ✅ `z-uo/female-LJSpeech-italian`
- ✅ `z-uo/male-LJSpeech-italian`
- ❌ `sololabs/ljspeech-italian` (non esiste)
- ❌ `giacomoarienti/...` (potrebbe essere rinominato)

### Dataset troppo grande per Colab

**Per dataset male (31h)**:
- Filtra subset: `split="train[:1000]"` (primi 1000 sample)
- Usa dataset female (più piccolo)
- Scarica localmente invece che su Colab

---

## 📋 Formato Dataset

Tutti i dataset seguono questo formato:

### Struttura File:
```
dataset/
├── wavs/
│   ├── LJ_000000.wav
│   ├── LJ_000001.wav
│   └── ...
└── metadata.csv
```

### Formato metadata.csv:
```
LJ_000000.wav|Testo della prima frase.
LJ_000001.wav|Testo della seconda frase.
...
```

**Separatore**: `|` (pipe)
**Colonne**: `filename|text`
**Encoding**: UTF-8

---

## 🎯 Quale Dataset Scegliere?

### Per Call Center / Assistenti Vocali:
✅ **z-uo/female-LJSpeech-italian**
- Voce professionale
- Dimensione gestibile
- Qualità eccellente
- Tempo training ragionevole

### Per Ricerca / Massima Qualità:
✅ **z-uo/male-LJSpeech-italian**
- Più ore di training
- Qualità superiore
- Richiede più tempo/GPU

### Per Variabilità Multi-Speaker:
✅ **sarulab-speech/commonvoice22_sidon**
- Molti speaker diversi
- Accenti variati
- Robustezza maggiore

---

## 📚 Risorse Aggiuntive

- **Piper TTS**: https://github.com/rhasspy/piper
- **Coqui TTS**: https://github.com/coqui-ai/TTS
- **Hugging Face Audio Datasets**: https://huggingface.co/datasets?task_categories=task_categories:text-to-speech
- **M-AILABS Dataset**: http://www.caito.de/2019/01/the-m-ailabs-speech-dataset/

---

## ⚖️ Licenze

- **z-uo datasets**: Derivati da M-AILABS (verifica licenza originale)
- **Common Voice**: CC0 (pubblico dominio)
- **MultilinguaLibriSpeech**: CC BY 4.0

⚠️ **IMPORTANTE**: Verifica sempre la licenza prima dell'uso commerciale!

---

## 🆘 Supporto

Problemi o domande? Apri una issue su GitHub o consulta:
- Script: `scripts/download_ljspeech_italian.py`
- Notebook: `Colab_FineTuning/Piper_Dataset_Preparation.ipynb`
- Documentazione Piper: https://github.com/rhasspy/piper
