# 📥 Download Dataset LJSpeech-Italian

## Problema: Solo 100 file scaricati invece di 5856

Se hai visto il messaggio:
```
✅ Trovati 5856 file audio
✅ Download completato! 📊 100 file audio salvati
```

Significa che è stato impostato un **limite di 100 file** nello script.

---

## ✅ SOLUZIONE: Scaricare TUTTI i 5856 file

### Opzione 1: Usa il notebook Colab aggiornato

1. Apri `Colab_FineTuning/Piper_Dataset_Preparation.ipynb`
2. Nella cella di download, verifica che sia impostato:
   ```python
   MAX_SAMPLES = None  # ⬅️ QUESTO SCARICA TUTTI I FILE!
   ```
3. Se era impostato `MAX_SAMPLES = 100`, cambialo in `None`
4. Esegui la cella

### Opzione 2: Usa lo script Python diretto

```bash
cd /home/user/Addestramento_Voce
python scripts/download_full_dataset.py
```

Questo script scaricherà **TUTTI** i 5856 file del dataset.

### Opzione 3: Usa lo script con parametri

```bash
cd /home/user/Addestramento_Voce

# Scarica TUTTO (nessun limite)
python scripts/download_ljspeech_italian.py \
  --output-dir /content/ljspeech_italian \
  --dataset z-uo/female-LJSpeech-italian

# Oppure per test (solo 100 file)
python scripts/download_ljspeech_italian.py \
  --output-dir /content/ljspeech_italian \
  --dataset z-uo/female-LJSpeech-italian \
  --max-samples 100
```

---

## 📊 Info Dataset

### z-uo/female-LJSpeech-italian
- **File**: 5856
- **Durata**: 8h 23m
- **Voce**: Femminile
- **Dimensione**: ~600 MB
- **Tempo download**: ~2 ore (con streaming mode)

### z-uo/male-LJSpeech-italian
- **File**: 13000+
- **Durata**: 31h 45m
- **Voce**: Maschile
- **Dimensione**: ~2.5 GB
- **Tempo download**: ~8 ore (con streaming mode)

---

## 🔍 Verifica Download

Dopo il download, verifica il numero di file:

```bash
# Su Colab
!ls -1 /content/ljspeech_italian/wavs | wc -l

# Dovrebbe mostrare: 5856 (per female) o 13000+ (per male)
```

Oppure controlla il metadata:
```bash
!wc -l /content/ljspeech_italian/metadata.csv
```

---

## ⚠️ Note Importanti

1. **Streaming Mode**: Lo script usa streaming mode per risparmiare RAM
2. **Google Drive**: Il notebook salva su `/content/drive/MyDrive/piper_training/dataset/`
3. **Memoria**: Richiede ~2-3 GB RAM liberi durante il download
4. **Tempo**: Download completo richiede 1-2 ore (female) o 6-8 ore (male)
5. **Interruzione**: Se il download si interrompe, riavvia e continuerà dal punto precedente

---

## 🆘 Problemi Comuni

### 1. Download si blocca dopo 100 file
**Causa**: `MAX_SAMPLES = 100` impostato nello script
**Soluzione**: Cambia in `MAX_SAMPLES = None`

### 2. Out of Memory
**Causa**: RAM insufficiente
**Soluzione**:
- Riavvia runtime Colab
- Verifica che streaming mode sia attivo (`streaming=True`)
- Chiudi altre tab/applicazioni

### 3. Errore HF_TOKEN
**Causa**: Token Hugging Face mancante
**Soluzione**:
- Crea file `.env` con `HF_TOKEN=your_token`
- Ottieni token da: https://huggingface.co/settings/tokens

### 4. Spazio disco insufficiente
**Causa**: Google Drive pieno
**Soluzione**:
- Libera spazio su Drive
- Cambia `output_dir` in directory locale `/content/ljspeech_italian`
