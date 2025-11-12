# 🚀 Fine-Tuning XTTS v2 su Google Colab

Guida completa per fine-tuning/training di modelli TTS usando Google Colab con GPU gratuita (T4 16GB VRAM).

---

## 📋 Indice

1. [Setup Iniziale](#setup-iniziale)
2. [Upload Notebook su Colab](#upload-notebook)
3. [Esecuzione Step-by-Step](#esecuzione)
4. [Download Risultati](#download-risultati)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

---

## 🎯 Cosa Faremo

### **Obiettivo:**
Preparare dataset Common Voice italiano e testare voice cloning con XTTS v2.

### **Nota Importante:**
Fine-tuning **completo** di XTTS v2 è complesso e richiede setup avanzato.
Questo notebook ti prepara per:
- ✅ Preprocessing dataset Common Voice IT
- ✅ Test voice cloning con dataset preprocessato
- ✅ Valutazione qualità
- ⚠️ Fine-tuning vero richiede repo Coqui completo

**Per uso immediato:** XTTS base + voice cloning funziona già benissimo! 🎉

---

## 🚀 Setup Iniziale

### **Step 1: Account Google**
- Serve Gmail account (gratuito)
- Vai su: https://colab.research.google.com/

### **Step 2: Limiti Colab FREE**
- ✅ **GPU T4** (16GB VRAM) - GRATIS
- ⚠️ Sessioni limitate: ~12 ore/giorno
- ⚠️ Timeout: 90 min inattività
- 💾 Storage: ~100GB temporaneo

**Pro ($10/mese):**
- Sessioni più lunghe (24h)
- GPU più potenti (V100, A100)
- Priorità accesso

---

## 📤 Upload Notebook su Colab

### **Metodo 1: Upload Diretto (CONSIGLIATO)**

1. Vai su: https://colab.research.google.com/
2. Click **"File" → "Upload notebook"**
3. Seleziona: `XTTS_FineTuning_Colab.ipynb`
4. Wait for upload
5. ✅ Pronto!

### **Metodo 2: Google Drive**

1. Upload notebook su Google Drive
2. Colab: "File" → "Open notebook" → "Google Drive"
3. Seleziona il file

### **Metodo 3: GitHub (avanzato)**

1. Fai fork/upload su tuo GitHub
2. Colab: "File" → "Open notebook" → "GitHub"
3. Incolla URL

---

## ▶️ Esecuzione Step-by-Step

### **Step 1: Seleziona GPU** ⚡

```
Runtime → Change runtime type → Hardware accelerator: GPU → Save
```

**Verifica GPU attiva:**
```python
!nvidia-smi
```

Dovresti vedere: `Tesla T4` (o simile)

---

### **Step 2: Esegui Celle in Ordine** 📝

**Cella 1 - Verifica GPU:**
- Esegui per controllare GPU disponibile
- Deve mostrare ~16GB VRAM

**Cella 2 - Install Dependencies:**
- Installa TTS, datasets, ecc.
- ⏱️ Tempo: ~2-3 minuti
- ⚠️ Potrebbe mostrare warnings (normali)

**Cella 3 - Import & Check:**
- Verifica librerie caricate
- Mostra info GPU

**Cella 4 - Configurazione:**
- **IMPORTANTE:** Modifica `num_samples` se vuoi:
  - `100` = test veloce (~5 min)
  - `1000` = training decente (~30 min)
  - `5000` = training serio (~2 ore)

**Cella 5 - Download Common Voice:**
- Scarica dataset italiano
- ⏱️ Tempo dipende da `num_samples`
- **Licenza CC0** = uso commerciale OK ✅

**Cella 6 - Preprocessing:**
- Converte audio a 22.05kHz
- Normalizza volume
- Crea metadata.csv
- ⏱️ Tempo: ~1-5 min per 1000 sample

**Cella 7 - Fine-Tuning Info:**
- Spiega limitazioni
- Mostra alternative
- Test modello base

**Celle 8-9 - Test & Download:**
- Testa voice cloning
- Download dataset preprocessato

---

### **Step 3: Monitora Progresso** 👀

**Durante esecuzione:**
- Celle mostrano progress bar
- Guarda uso VRAM:
  ```python
  !nvidia-smi
  ```
- Se VRAM piena → riduci `batch_size`

**Indicatori successo:**
- ✅ Checkmarks verdi
- ✅ "Completato" nei print
- ❌ Errori rossi → vedi Troubleshooting

---

## 📥 Download Risultati

### **Cosa Scaricare:**

**1. Dataset Preprocessato** (importante!)
```python
files.download("/content/dataset_prepared.zip")
```
- Contiene audio processati + metadata
- Riutilizzabile localmente
- **Salva questo file!**

**2. Audio Test**
```python
files.download("/content/test_speaker_0.wav")
files.download("/content/test_speaker_1.wav")
files.download("/content/test_speaker_2.wav")
```
- Esempi voice cloning
- Confronta qualità

**3. (Se training completo) Modello**
```python
files.download("/content/xtts_finetuned/best_model.pth")
```
- Solo se fai training avanzato
- Poi usa localmente

---

## 🔧 Troubleshooting

### **1. GPU Non Disponibile**

**Errore:** "GPU not available"

**Soluzioni:**
- Runtime → Change runtime type → GPU
- Se ancora errore: Colab usage limits reached
- Wait 12-24 ore o usa Colab Pro

---

### **2. Out of Memory (OOM)**

**Errore:** "CUDA out of memory"

**Soluzioni:**
```python
# Riduci batch_size in CONFIG
"batch_size": 1,  # invece di 2

# Riduci num_samples
"num_samples": 500,  # invece di 1000
```

---

### **3. Dataset Download Lento**

**Problema:** Common Voice download molto lento

**Soluzioni:**
- Riduci `num_samples` temporaneamente
- Prova in orari meno traffico (notte EU)
- Usa dataset più piccolo per test

---

### **4. Sessione Interrotta**

**Problema:** Colab disconnette dopo 90 min inattività

**Soluzioni:**
- Clicca periodicamente nella pagina
- Usa script auto-click (Tampermonkey)
- Upgrade a Colab Pro

---

### **5. File Persi dopo Disconnessione**

**Problema:** File `/content/` spariscono

**Soluzioni:**
- **SALVA su Google Drive:**
  ```python
  from google.colab import drive
  drive.mount('/content/drive')

  # Salva qui invece:
  "/content/drive/MyDrive/xtts_project/"
  ```

- **Download frequenti:**
  - Scarica output importanti subito
  - Non lasciare file solo in `/content/`

---

## ❓ FAQ

### **Q: Quanto tempo serve?**

**A:** Dipende da obiettivo:
- Test preprocessing: ~10-15 min
- Voice cloning test: ~5 min
- Fine-tuning vero XTTS: 10-20 ore

### **Q: Posso usare dataset custom?**

**A:** Sì! Modifica notebook:
```python
# Invece di Common Voice:
# 1. Upload tuo dataset su Colab
# 2. Modifica path in CONFIG
# 3. Assicurati formato corretto (audio + trascrizioni)
```

### **Q: Colab è legale per commerciale?**

**A:** Sì, Colab FREE:
- ✅ OK per progetti commerciali
- ✅ OK training modelli vendibili
- ⚠️ Non per mining crypto
- ⚠️ Rispetta Terms of Service

**Dataset Common Voice:** CC0 = commerciale OK ✅

### **Q: Serve fine-tuning o basta voice cloning?**

**A:** Per call center italiano:
- **Voice cloning (no training):** ✅ Sufficiente per 90% casi
  - Qualità già ottima (9/10)
  - Funziona subito
  - Zero training time

- **Fine-tuning (con training):** Solo se:
  - Hai termini tecnici molto specifici
  - Vuoi pronuncia perfetta assoluta
  - Hai tempo/budget per 10-20h training

**Consiglio:** Inizia con voice cloning, valuta se serve fine-tuning.

### **Q: Posso interrompere e riprendere?**

**A:** ⚠️ Difficile su Colab FREE:
- Sessioni sono temporanee
- File `/content/` si perdono
- **Soluzione:** Salva checkpoint su Drive

### **Q: Qual è la differenza tra questo e training locale?**

**A:**

| Aspetto | Colab FREE | Locale (3050Ti 4GB) |
|---------|------------|---------------------|
| **VRAM** | 16GB T4 | 4GB |
| **Training XTTS** | ✅ Possibile | ❌ OOM |
| **Costo** | Gratis | 0€ |
| **Velocità** | Veloce | N/A |
| **Limiti sessione** | 12h/giorno | Illimitato |
| **Storage** | ~100GB temp | Il tuo |

**Best practice:** Training su Colab → Inferenza locale

### **Q: Alternative a Colab?**

**A:** Altri servizi simili:
- **Kaggle Notebooks** (30h/week FREE)
- **Paperspace Gradient** (FREE tier)
- **Vast.ai** (GPU rental $0.20-0.50/h)
- **RunPod** (simile Vast.ai)

---

## 🎯 Prossimi Passi

Dopo aver completato questo notebook:

### **1. Hai Dataset Preprocessato ✅**
- Salvato in `dataset_prepared.zip`
- Pronto per uso locale
- Riutilizzabile per altri training

### **2. Voice Cloning Funziona ✅**
- Usi XTTS base
- Con sample voce (10s)
- Qualità 9/10

### **3. Se Vuoi Fine-Tuning Vero:**

**Opzione A - Training XTTS Completo (Avanzato):**
```bash
# Clone repo Coqui
git clone https://github.com/coqui-ai/TTS
cd TTS

# Segui recipe XTTS
# recipes/ljspeech/xtts_v2/train_xtts.py

# Adatta per Common Voice IT
# 10-20 ore training su Colab
```

**Opzione B - Training VITS (Più Semplice):**
```bash
# Clone repo VITS
git clone https://github.com/jaywalnut310/vits

# Training più accessibile
# 5-10 ore
# Qualità buona (8/10)
```

**Opzione C - Continua Voice Cloning (RACCOMANDATO):**
```python
# Usa XTTS base già funzionante
# Qualità 9/10 già ottima
# Zero training time
# Perfetto per produzione
```

---

## 📚 Risorse Utili

**Coqui TTS:**
- Repo: https://github.com/coqui-ai/TTS
- Docs: https://tts.readthedocs.io/
- Recipes: https://github.com/coqui-ai/TTS/tree/dev/recipes

**Common Voice:**
- Dataset: https://huggingface.co/datasets/mozilla-foundation/common_voice_11_0
- Licenza: https://creativecommons.org/publicdomain/zero/1.0/

**Google Colab:**
- FAQ: https://research.google.com/colaboratory/faq.html
- Pro: https://colab.research.google.com/signup

---

## 💡 Tips & Tricks

**1. Risparmia tempo Colab:**
- Testa con `num_samples=100` prima
- Poi aumenta per training serio

**2. Backup frequenti:**
- Salva su Google Drive periodicamente
- Download output importanti subito

**3. Monitora VRAM:**
```python
!watch -n 1 nvidia-smi  # Monitora ogni 1 secondo
```

**4. Parallelize download:**
- Scarica Common Voice mentre test altri modelli

**5. Documenta config:**
- Salva JSON con parametri usati
- Utile per riprodurre risultati

---

## 🎉 Buon Training!

Hai domande? Controlla:
1. FAQ sopra
2. Troubleshooting
3. Commenti nel notebook

**Happy Fine-Tuning! 🚀**
