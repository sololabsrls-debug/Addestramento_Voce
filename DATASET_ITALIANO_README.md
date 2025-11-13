# 🇮🇹 Dataset LJSpeech-Italiano

## ✅ Dataset Scaricato

**Dataset:** `z-uo/female-LJSpeech-italian`
**Fonte:** Hugging Face
**Licenza:** Pubblico dominio (testi da I Malavoglia di Giovanni Verga)

---

## 📊 Statistiche

| Metrica | Valore |
|---------|--------|
| **File audio** | 5856 WAV |
| **Durata totale** | 8h 23m 55s |
| **Durata media** | 5.16s per file |
| **Sample rate** | 16000Hz |
| **Formato** | WAV mono |
| **Lingua** | Italiano |

---

## 📂 Struttura

```
ljspeech_italian/
├── wavs/                              5856 file audio
│   ├── imalavoglia_00_verga_f000001.wav
│   ├── imalavoglia_00_verga_f000002.wav
│   └── ...
├── metadata.csv                       5856 righe
└── metadata_mls.json                  Metadata aggiuntivi
```

---

## 📄 Formato metadata.csv

Ogni riga ha 3 colonne separate da `|`:

```
filename|testo_originale|testo_normalizzato
```

**Esempio:**
```
imalavoglia_00_verga_f000001|Prefazione.|Prefazione.
imalavoglia_00_verga_f000002|Questo racconto è lo studio...|Questo racconto è lo studio...
```

**Colonne:**
1. **filename**: Nome file SENZA estensione `.wav`
2. **testo_originale**: Testo con punteggiatura originale
3. **testo_normalizzato**: Testo normalizzato per TTS

---

## 🚀 Come Scaricare

### Metodo 1: Download Completo (RACCOMANDATO)

```python
from huggingface_hub import snapshot_download, login

# Autenticazione
HF_TOKEN = "your_token_here"
login(token=HF_TOKEN)

# Download
local_dir = snapshot_download(
    repo_id="z-uo/female-LJSpeech-italian",
    repo_type="dataset",
    token=HF_TOKEN,
    local_dir="/content/ljspeech_italian"
)
```

**Vantaggi:**
- ✅ Non crasha (no `load_dataset()`)
- ✅ Bypassa CSV malformato
- ✅ Download diretto via Git LFS
- ✅ Tempo: ~3-5 minuti

### Metodo 2: Script Automatico

```bash
cd /home/user/Addestramento_Voce
python download_dataset_italiano.py
```

---

## 🔍 Verifica Dataset

Dopo il download, verifica l'integrità:

```bash
python verifica_dataset_italiano.py /content/ljspeech_italian
```

Output atteso:
```
✅ Corrispondenza perfetta!
📊 File totali: 5856
⏱️  Durata totale: 8h 23m 55s
🇮🇹 Lingua: ITALIANO
```

---

## 🎯 Uso per Training

### Coqui TTS (XTTS v2)

Il dataset è compatibile con:
- Fine-tuning XTTS v2
- Voice cloning
- Multi-speaker training

**Preprocessing richiesto:**
- Resample a 22050Hz (se necessario)
- Creazione file `metadata.csv` formato Coqui

### Piper TTS

**Preprocessing richiesto:**
- Verifica sample rate 16000Hz ✅ (già corretto)
- Formato metadata compatibile ✅
- Generazione phonemes

---

## ⚠️ Note Importanti

### 1. Problema CSV Malformato

Il `metadata.csv` del dataset ha un bug di parsing che impedisce l'uso di `load_dataset()`:

```
ParserError: Expected 1 fields in line 5, saw 5
```

**Soluzione:** Usa `snapshot_download()` invece di `load_dataset()`

### 2. Sample Rate

Il dataset è a **16000Hz**, non 22050Hz come LJSpeech originale.

**Per Coqui TTS:** Resample a 22050Hz prima del training:
```python
import librosa
import soundfile as sf

data, sr = librosa.load("input.wav", sr=16000)
data_resampled = librosa.resample(data, orig_sr=16000, target_sr=22050)
sf.write("output.wav", data_resampled, 22050)
```

**Per Piper TTS:** 16000Hz è perfetto ✅

---

## 🆚 Confronto con LJSpeech Originale

| Caratteristica | LJSpeech (EN) | LJSpeech-Italian |
|----------------|---------------|------------------|
| **Lingua** | Inglese | Italiano 🇮🇹 |
| **File** | 13100 | 5856 |
| **Durata** | 24h | 8h 23m |
| **Sample rate** | 22050Hz | 16000Hz |
| **Voce** | Femminile | Femminile |
| **Fonte testi** | Libri pubblico dominio | I Malavoglia |

---

## 🔗 Alternative Dataset Italiano

Se questo dataset non è sufficiente:

1. **z-uo/male-LJSpeech-italian**
   - 13000+ file
   - 31h 45m di audio
   - Voce maschile

2. **Mozilla Common Voice (IT)**
   - Multi-speaker
   - Diverse età/accenti
   - Pubblico dominio

3. **M-AILABS Italian**
   - Alta qualità
   - Multiple voci
   - Controllare licenza

---

## 📧 Link Utili

- **Hugging Face:** https://huggingface.co/datasets/z-uo/female-LJSpeech-italian
- **Dataset maschile:** https://huggingface.co/datasets/z-uo/male-LJSpeech-italian
- **Token HF:** https://huggingface.co/settings/tokens

---

## ✅ Checklist Post-Download

- [x] 5856 file WAV scaricati
- [x] metadata.csv presente
- [x] Testi in italiano verificati
- [x] Sample rate 16000Hz confermato
- [ ] Backup su Google Drive
- [ ] Preprocessing per TTS
- [ ] Training modello

---

**Ultima verifica:** 2025-11-13
**Status:** ✅ Pronto per il training
