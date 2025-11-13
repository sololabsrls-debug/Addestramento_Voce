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

### Opzione 3: Usa lo script con parametri (CONSIGLIATO)

```bash
cd /home/user/Addestramento_Voce

# Scarica TUTTO (nessun limite) con retry automatico e checkpoint
python scripts/download_ljspeech_italian.py \
  --output-dir /content/ljspeech_italian \
  --dataset z-uo/female-LJSpeech-italian

# Oppure per test (solo 100 file)
python scripts/download_ljspeech_italian.py \
  --output-dir /content/ljspeech_italian \
  --dataset z-uo/female-LJSpeech-italian \
  --max-samples 100

# Ricomincia da zero (ignora checkpoint)
python scripts/download_ljspeech_italian.py \
  --output-dir /content/ljspeech_italian \
  --dataset z-uo/female-LJSpeech-italian \
  --no-resume
```

### 🆕 Nuove Funzionalità

Lo script è stato migliorato con:

1. **Retry Logic Automatico**
   - Ritenta automaticamente in caso di errori di rete
   - Backoff esponenziale: 2s, 4s, 8s, 16s, 32s
   - Gestione intelligente dei rate limits

2. **Checkpoint System**
   - Salva progressi ogni 50 file
   - Riprende automaticamente da dove si è interrotto
   - Checkpoint salvato in `.checkpoint.json`

3. **Rate Limit Handling**
   - Pausa automatica quando Hugging Face applica rate limits
   - Attesa crescente: 5s, 10s, 20s, 40s... fino a 300s
   - Continua automaticamente dopo l'attesa

4. **Monitoraggio RAM**
   - Visualizza uso RAM ogni 50 file
   - Garbage collection automatica ogni 100 file
   - Ottimizzato per evitare Out of Memory

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

### 1. Rate Limit (429 Error)
**Causa**: Troppe richieste a Hugging Face
**Soluzione**: ✅ **Gestito automaticamente!**
- Lo script pausa automaticamente
- Riprende dopo attesa crescente (5s, 10s, 20s...)
- Non serve fare nulla, aspetta

### 2. Errore di rete / Connection Timeout
**Causa**: Problemi di connessione temporanei
**Soluzione**: ✅ **Gestito automaticamente!**
- Retry automatico con backoff esponenziale
- Fino a 5 tentativi per operazione
- Checkpoint salva progressi ogni 50 file

### 3. Download interrotto
**Causa**: Crash, chiusura terminale, ecc.
**Soluzione**: ✅ **Gestito automaticamente!**
- Riesegui lo stesso comando
- Lo script riprende dall'ultimo checkpoint
- Non riscaricare file già salvati

### 4. Download si blocca dopo 100 file
**Causa**: `MAX_SAMPLES = 100` impostato nello script
**Soluzione**: Cambia in `MAX_SAMPLES = None` o usa `--max-samples` senza valore

### 5. Out of Memory
**Causa**: RAM insufficiente
**Soluzione**:
- ✅ Monitoraggio RAM integrato (visualizzato ogni 50 file)
- Verifica che streaming mode sia attivo (`streaming=True`)
- Riavvia runtime Colab se necessario
- Chiudi altre tab/applicazioni

### 6. Errore HF_TOKEN
**Causa**: Token Hugging Face mancante o non valido
**Soluzione**:
- Crea file `.env` con `HF_TOKEN=your_token`
- Ottieni token da: https://huggingface.co/settings/tokens
- Verifica che il token sia valido

### 7. Spazio disco insufficiente
**Causa**: Google Drive pieno
**Soluzione**:
- Libera spazio su Drive
- Cambia `output_dir` in directory locale `/content/ljspeech_italian`

### 8. Troppi errori consecutivi
**Causa**: Dataset corrotto o problemi persistenti
**Soluzione**:
- Verifica connessione internet stabile
- Controlla logs per pattern di errore
- Prova `--no-resume` per ricominciare da zero
