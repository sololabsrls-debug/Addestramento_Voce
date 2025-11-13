# 🛠️ Troubleshooting - Dataset Download

Guida alla risoluzione dei problemi comuni durante il download del dataset LJSpeech-Italian.

---

## ❌ Errore: Out of Memory (OOM) / Crash Runtime

### Sintomi:
```
std::bad_alloc
terminate called after throwing an instance of 'std::bad_alloc'
AsyncIOLoopKernelRestarter: restarting kernel (1/5)
Si è verificato un arresto anomalo della sessione
```

### Causa:
Il dataset viene caricato completamente in RAM oppure il download esaurisce la memoria disponibile anche in streaming mode. Google Colab Free (~12GB RAM) può esaurire la memoria con dataset grandi.

### ✅ SOLUZIONE 1: Usa Memory-Safe Mode (RACCOMANDATO)

**AGGIORNAMENTO 2025-11-13**: Il notebook `Piper_Dataset_Preparation.ipynb` è stato aggiornato con protezioni avanzate memoria:

**Nuove funzionalità:**
- Controllo automatico RAM ogni 10 file
- Stop automatico se RAM < 2GB
- Resume capability (riprende da dove si è fermato)
- Batch size ridotto (50 invece di 100)
- Pause tra i batch per liberare memoria
- Statistiche RAM in tempo reale

**Limitazione default per sicurezza:**
Il notebook ora usa `MAX_SAMPLES = 1000` per default invece di scaricare tutto. Questo previene crash su Colab Free.

Per scaricare l'intero dataset:
1. Verifica di avere >8GB RAM disponibili
2. Cambia `MAX_SAMPLES = None` nel notebook
3. Monitora l'uso RAM durante il download
4. Se si ferma, riesegui la cella: riprenderà automaticamente

### ✅ SOLUZIONE 2: Usa Streaming Mode (Versione Base)

**Cella corretta con streaming:**

```python
# ============================================================
#  DOWNLOAD LJSPEECH-IT - VERSIONE OTTIMIZZATA (LOW MEMORY)
# ============================================================

print("="*60)
print("  DOWNLOAD LJSPEECH-IT - STREAMING MODE")
print("="*60)
print()

import os
from datasets import load_dataset
from tqdm import tqdm
import soundfile as sf
import gc  # Garbage collector per liberare memoria

# Installa torchcodec se mancante
try:
    import torchcodec
except ImportError:
    print("📦 Installazione torchcodec...")
    !pip install -q torchcodec
    print("✅ torchcodec installato")

# Scegli dataset
DATASET_NAME = "z-uo/female-LJSpeech-italian"  # 8h 23m, voce femminile
# DATASET_NAME = "z-uo/male-LJSpeech-italian"  # 31h 45m, voce maschile

# OPZIONALE: Limita numero di sample per test (None = tutti)
MAX_SAMPLES = None  # Cambia in 100, 500, 1000 per test rapidi
# MAX_SAMPLES = 500  # Decommenta per processare solo 500 sample

print(f"📥 Scaricamento dataset: {DATASET_NAME}...")
print("💡 Uso streaming mode per risparmiare memoria")

# Carica in STREAMING MODE per non saturare la RAM
dataset = load_dataset(DATASET_NAME, split="train", streaming=True)

# Crea directory su Drive
dataset_dir = "/content/drive/MyDrive/piper_training/dataset/ljspeech_italian"
wavs_dir = os.path.join(dataset_dir, "wavs")
os.makedirs(wavs_dir, exist_ok=True)

print(f"\n💾 Salvataggio su Google Drive...")
print(f"📁 Percorso: {dataset_dir}")

# Prepara metadata
metadata_lines = []
processed = 0

# Processa sample uno alla volta (streaming)
for idx, item in enumerate(tqdm(dataset, desc="Salvando audio")):
    try:
        # Limita numero di sample se richiesto
        if MAX_SAMPLES and idx >= MAX_SAMPLES:
            print(f"\n⏸️  Limite raggiunto: {MAX_SAMPLES} sample processati")
            break

        # Salva audio
        audio_filename = f"LJ_{idx:06d}.wav"
        audio_path = os.path.join(wavs_dir, audio_filename)

        # Estrai audio array e sample rate
        audio_data = item['audio']
        sf.write(audio_path, audio_data['array'], audio_data['sampling_rate'])

        # Aggiungi a metadata
        text = item['text']
        metadata_lines.append(f"{audio_filename}|{text}")

        processed += 1

        # Libera memoria ogni 100 file
        if processed % 100 == 0:
            gc.collect()

    except Exception as e:
        print(f"\n⚠️  Errore sample {idx}: {e}")
        continue

# Salva metadata.csv
metadata_path = os.path.join(dataset_dir, "metadata.csv")
with open(metadata_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(metadata_lines))

print(f"\n✅ Completato!")
print(f"   📊 {processed} file audio salvati")
print(f"   📄 metadata.csv creato")
print(f"   💾 Totale: ~{processed * 0.5:.1f} MB")
print(f"\n📋 Dataset usato: {DATASET_NAME}")
print(f"   🎤 Tipo: {'Voce femminile' if 'female' in DATASET_NAME else 'Voce maschile'}")

# Libera memoria finale
del dataset
gc.collect()
```

### ✅ SOLUZIONE 3: Limita Sample per Test

Il notebook aggiornato usa già `MAX_SAMPLES = 1000` per default. Per test più rapidi:

```python
MAX_SAMPLES = 100   # Solo 100 sample (veloce, ~5-10 min)
MAX_SAMPLES = 500   # 500 sample (medio, ~20-30 min)
MAX_SAMPLES = 1000  # 1000 sample (default, ~40-60 min)
MAX_SAMPLES = None  # Tutti (completo, ~2-3 ore, usa con cautela)
```

**Nota**: Con il nuovo memory-safe mode, anche `MAX_SAMPLES = None` dovrebbe funzionare su Colab Free, ma si fermerà automaticamente se la RAM scende troppo.

### ✅ SOLUZIONE 4: Riavvia Runtime

Prima di eseguire il download:

1. **Runtime** → **Restart runtime**
2. Esegui solo le celle necessarie:
   - Monta Drive
   - Installa dipendenze
   - Download dataset
3. NON eseguire altre celle pesanti prima del download

### ✅ SOLUZIONE 5: Verifica RAM Prima di Iniziare

Il notebook aggiornato include già una cella di verifica RAM (cella 5). Eseguila prima del download:

```python
import psutil

ram_available = psutil.virtual_memory().available / 1e9
print(f"💾 RAM disponibile: {ram_available:.1f} GB")

if ram_available < 5:
    print("⚠️  RAM BASSA! Usa MAX_SAMPLES=500 o riavvia runtime")
else:
    print("✅ RAM sufficiente")
```

**Nuovo**: Il download si ferma automaticamente se RAM < 2GB durante l'esecuzione.

### ✅ SOLUZIONE 6: Scarica Localmente (NON su Colab)

Se hai un PC con più RAM:

```bash
# Installa dipendenze
pip install datasets soundfile tqdm torchcodec

# Esegui script
python scripts/download_ljspeech_italian.py \
  --dataset z-uo/female-LJSpeech-italian \
  --output-dir ./dataset/ljspeech_italian
```

**Opzioni aggiuntive:**
```bash
# Solo 500 sample
python scripts/download_ljspeech_italian.py \
  --dataset z-uo/female-LJSpeech-italian \
  --max-samples 500 \
  --output-dir ./dataset

# Disabilita streaming (se hai >16GB RAM)
python scripts/download_ljspeech_italian.py \
  --dataset z-uo/male-LJSpeech-italian \
  --no-streaming \
  --output-dir ./dataset
```

---

## ❌ Errore: ImportError torchcodec

### Sintomi:
```
ImportError: To support decoding audio data, please install 'torchcodec'
```

### ✅ Soluzione:

La cella corretta include auto-installazione:

```python
try:
    import torchcodec
except ImportError:
    print("📦 Installazione torchcodec...")
    !pip install -q torchcodec
    print("✅ torchcodec installato")
```

Oppure installa manualmente:
```python
!pip install -q torchcodec
```

---

## ❌ Errore: DatasetNotFoundError

### Sintomi:
```
DatasetNotFoundError: Dataset 'sololabs/ljspeech-italian' doesn't exist
```

### ✅ Soluzione:

Usa i nomi corretti:

```python
# ✅ CORRETTO
DATASET_NAME = "z-uo/female-LJSpeech-italian"
DATASET_NAME = "z-uo/male-LJSpeech-italian"

# ❌ SBAGLIATO
DATASET_NAME = "sololabs/ljspeech-italian"  # NON ESISTE!
```

---

## ❌ Errore: Campo 'sentence' non trovato

### Sintomi:
```
KeyError: 'sentence'
```

### ✅ Soluzione:

Usa `item['text']` invece di `item['sentence']`:

```python
# ✅ CORRETTO
text = item['text']

# ❌ SBAGLIATO
text = item['sentence']
```

---

## ❌ Timeout o Disconnessione

### Sintomi:
- Colab si disconnette durante download
- Timeout dopo 90 minuti

### ✅ Soluzione 1: Mantieni Attiva la Sessione

Apri console browser (F12) e incolla:

```javascript
function KeepAlive() {
  console.log("Keeping session alive...");
  document.querySelector("colab-connect-button").click();
}
setInterval(KeepAlive, 60000); // Ogni 60 secondi
```

### ✅ Soluzione 2: Usa Colab Pro

- Timeout più lunghi
- Più RAM (fino a 25GB)
- GPU migliori

### ✅ Soluzione 3: Download in Batch

Scarica in più sessioni:

```python
# Sessione 1: primi 500
MAX_SAMPLES = 500
# ... esegui download

# Sessione 2: successivi 500 (modifica codice per offset)
START_IDX = 500
MAX_SAMPLES = 1000
```

---

## ❌ Spazio Drive Insufficiente

### Sintomi:
```
No space left on device
```

### ✅ Soluzione:

**Spazio richiesto:**
- Female dataset: ~600 MB
- Male dataset: ~2.5 GB

**Libera spazio su Drive:**
1. Elimina file vecchi
2. Usa account Google con più spazio
3. Salva in directory locale `/content/dataset` (temporaneo)

```python
# Salva in locale invece che Drive
dataset_dir = "/content/dataset/ljspeech_italian"
```

⚠️ **NOTA**: Files in `/content/` vengono persi quando il runtime termina!

---

## ❌ Errore di Lettura/Scrittura Drive

### Sintomi:
```
Permission denied
OSError: [Errno 5] Input/output error
```

### ✅ Soluzione:

1. **Riconnetti Drive:**
```python
from google.colab import drive
drive.flush_and_unmount()
drive.mount('/content/drive', force_remount=True)
```

2. **Verifica permessi:**
```python
import os
test_file = "/content/drive/MyDrive/test.txt"
try:
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    print("✅ Permessi OK")
except Exception as e:
    print(f"❌ Errore permessi: {e}")
```

---

## 📊 Requisiti Sistema

### Google Colab Free:
- ✅ RAM: ~12GB (usa streaming mode)
- ✅ GPU: T4 o superiore (non necessaria per download)
- ✅ Disco: 15GB liberi
- ⚠️ Timeout: 90 minuti (riconnetti periodicamente)

### Google Colab Pro:
- ✅ RAM: fino a 25GB
- ✅ Timeout: più lunghi
- ✅ GPU: A100, V100
- ✅ Raccomandato per dataset male (31h)

### Locale (PC):
- ✅ RAM: 8GB+ (16GB raccomandati per no-streaming)
- ✅ Disco: 5GB liberi
- ✅ Python 3.8+

---

## 🎯 Configurazioni Consigliate

### Per Test Rapido (10 minuti):
```python
DATASET_NAME = "z-uo/female-LJSpeech-italian"
MAX_SAMPLES = 100
streaming = True
```

### Per Dataset Medio (1 ora):
```python
DATASET_NAME = "z-uo/female-LJSpeech-italian"
MAX_SAMPLES = 1000
streaming = True
```

### Per Dataset Completo Female (2-3 ore):
```python
DATASET_NAME = "z-uo/female-LJSpeech-italian"
MAX_SAMPLES = None
streaming = True
```

### Per Dataset Completo Male (8-12 ore):
```python
DATASET_NAME = "z-uo/male-LJSpeech-italian"
MAX_SAMPLES = None
streaming = True
# Raccomandato: Usa Colab Pro o locale
```

---

## 📞 Supporto

Se i problemi persistono:

1. Verifica di usare il **notebook aggiornato**: `Colab_FineTuning/Piper_Dataset_Preparation.ipynb`
2. Verifica di usare lo **script aggiornato**: `scripts/download_ljspeech_italian.py`
3. Leggi `DATASET_INFO.md` per dettagli sui dataset
4. Apri una issue su GitHub con:
   - Errore completo
   - RAM disponibile (`psutil.virtual_memory().available / 1e9`)
   - Dataset usato
   - Parametri usati

---

## ✅ Checklist Pre-Download

Prima di iniziare, verifica:

- [ ] Runtime Colab riavviato di recente
- [ ] Google Drive montato correttamente
- [ ] RAM disponibile > 5GB
- [ ] Spazio Drive > 3GB
- [ ] Torchcodec installato (auto-installato dalla cella)
- [ ] Dataset name corretto (`z-uo/...`)
- [ ] Streaming mode attivato (`streaming=True`)
- [ ] MAX_SAMPLES configurato per test iniziale

---

## 🚀 Quick Fix Universale

Se nulla funziona, usa questa versione minima garantita:

```python
# VERSIONE ULTRA-SAFE - SEMPRE FUNZIONA
import os
from datasets import load_dataset
from tqdm import tqdm
import soundfile as sf
import gc

# Solo 50 sample per test
MAX_SAMPLES = 50

dataset = load_dataset("z-uo/female-LJSpeech-italian", split="train", streaming=True)

dataset_dir = "/content/dataset_test"
os.makedirs(f"{dataset_dir}/wavs", exist_ok=True)

metadata = []
for idx, item in enumerate(dataset):
    if idx >= MAX_SAMPLES:
        break

    audio_file = f"LJ_{idx:06d}.wav"
    sf.write(f"{dataset_dir}/wavs/{audio_file}", item['audio']['array'], item['audio']['sampling_rate'])
    metadata.append(f"{audio_file}|{item['text']}")

    if idx % 10 == 0:
        gc.collect()

with open(f"{dataset_dir}/metadata.csv", 'w') as f:
    f.write('\n'.join(metadata))

print(f"✅ Completato: {MAX_SAMPLES} sample salvati in {dataset_dir}")
```

Questa versione:
- ✅ Solo 50 sample (velocissimo)
- ✅ Streaming mode
- ✅ Garbage collection
- ✅ Minimo uso RAM
- ✅ Funziona sempre

Aumenta `MAX_SAMPLES` gradualmente dopo aver verificato che funziona.
