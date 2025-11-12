# 🎤 Addestramento Voce - TTS Training Project

Progetto completo per testing, training e deployment di modelli Text-to-Speech (TTS) in italiano per applicazioni commerciali (call center, assistenti virtuali, etc.).

## ⚠️ IMPORTANTE - Google Colab + Python 3.12

**Google Colab ha aggiornato a Python 3.12, ma TTS richiede Python ≤ 3.11**

✅ **SOLUZIONE:** Vedi `Colab_FineTuning/SOLUZIONI_PYTHON312.md` per notebook aggiornati!

---

## 📊 Modelli Testati

| Modello | Qualità | RTF | Latenza | Uso Commerciale | Status |
|---------|---------|-----|---------|-----------------|--------|
| **Coqui XTTS v2** | 9/10 | 1.36 | ~2s | ✅ Sì (MIT) | ✅ Testato |
| **Azzurra-voice** | 10/10 | 43.5 | ~30s | ❌ No (CC-BY-NC) | ✅ Scaricato |
| **Resemble Chatterbox** | 8.5/10 | 0.8 | <1s | ✅ Sì | ⏳ Da testare |

**RTF** = Real-Time Factor (1.0 = tempo reale, <1.0 = più veloce)

## 📂 Struttura Progetto

```
Addestramento_Voce/
├── Colab_FineTuning/                     🚀 TRAINING SU GOOGLE COLAB
│   ├── SOLUZIONI_PYTHON312.md            ⚠️ LEGGI PRIMA (fix Python 3.12)
│   ├── XTTS_Colab_Alternativa.ipynb      ⚡ Notebook veloce (5 min)
│   ├── XTTS_Colab_Python311.ipynb        🐍 Notebook affidabile (10 min)
│   ├── XTTS_FineTuning_Colab.ipynb       Notebook completo
│   ├── XTTS_Test_Semplice.ipynb          Test semplificato
│   ├── INDEX.md                          Guida navigazione
│   ├── README.md                         Documentazione completa
│   ├── QUICK_START.md                    Start rapido
│   └── docs/NOTE_TECNICHE.md             Approfondimenti
│
├── CoquiXTTS/                            TEST LOCALE XTTS v2
│   ├── scripts/
│   │   ├── download_model.py
│   │   └── test_quick.py                 ✅ Testato
│   ├── audio_output/
│   │   └── test_30sec.wav                ✅ Generato
│   ├── voices/
│   │   └── voce_riferimento_converted.wav
│   └── config/
│
├── Azzurra/                              TEST LOCALE AZZURRA
│   ├── scripts/
│   │   ├── download_model.py             ✅ Completato
│   │   └── test_quick.py
│   ├── models/azzurra-voice/             ✅ Scaricato (13 file)
│   └── audio_output/
│
├── voci_riferimento/                     CAMPIONI VOCE
│   └── Addestramento_Voce.wav
│
└── testo_test_30sec.txt                  TESTO TEST
```

## 🚀 Quick Start

### **Opzione 1: Training su Google Colab** (RACCOMANDATO) ⚡

**Per fine-tuning o preprocessing dataset:**

1. **Apri** `Colab_FineTuning/SOLUZIONI_PYTHON312.md`
2. **Scegli** notebook:
   - `XTTS_Colab_Alternativa.ipynb` (veloce, 5 min)
   - `XTTS_Colab_Python311.ipynb` (affidabile, 10 min)
3. **Upload** su https://colab.research.google.com/
4. **Attiva** GPU: Runtime → Change runtime type → GPU
5. **Esegui** celle in ordine

**Risultato:** Dataset preprocessato + modello XTTS funzionante

---

### **Opzione 2: Voice Cloning Locale** (IMMEDIATO) 🎯

**Per generare audio subito:**

```bash
# Clone repository
git clone https://github.com/sololabsrls-debug/Addestramento_Voce.git
cd Addestramento_Voce

# Installa dipendenze (Python 3.11!)
pip install TTS==0.22.0 soundfile

# Test XTTS v2
cd CoquiXTTS/scripts
python test_quick.py
```

**Risultato:** Audio generato in ~1 minuto (RTF 1.36x)

---

### **Opzione 3: Test Azzurra** (QUALITÀ MASSIMA) 🏆

```bash
cd Azzurra/scripts

# Download modello (solo prima volta, ~5 min)
python download_model.py

# Test generazione
python test_quick.py
```

**Nota:** ⚠️ Solo uso non commerciale (CC-BY-NC)

## Metriche Misurate

- **Tempo di sintesi**: Tempo totale per generare audio
- **RTF (Real-Time Factor)**: Rapporto tempo_sintesi/durata_audio
  - RTF < 1.0 = Più veloce del tempo reale (ideale)
  - RTF > 1.0 = Più lento del tempo reale
- **Qualità**: Valutazione dal PDF di ricerca (scala 1-10)
- **Dimensione file**: Dimensione output audio

## Requisiti Sistema

- Python 3.8+
- GPU CUDA (opzionale ma raccomandato)
- Spazio disco: ~5-10GB per i modelli
- RAM: 8GB+ raccomandato

## Note

- **Azzurra-voice**: Migliore qualità per italiano
- **Coqui XTTS v2**: Ottimo compromesso, multilingua
- **Resemble Chatterbox**: Migliore per latenza bassa (chiamate real-time)

## Riferimenti

- Analisi completa: `Modelli TTS Locali per Chiamate in Italiano – Ricerca Completa.pdf`
- Azzurra: https://huggingface.co/Azurro/Azzurra-voice
- Coqui XTTS: https://github.com/coqui-ai/TTS
- Resemble: https://github.com/resemble-ai

## Troubleshooting

### Errore CUDA/GPU
Se non hai GPU, i modelli useranno CPU (più lento). È normale.

### Modello non trovato
Assicurati di aver eseguito `download_model.py` prima di `test_tts.py`

### Dipendenze mancanti
```bash
pip install -r requirements.txt
```

## 📄 Licenze

**Progetto:** MIT License (uso commerciale OK)

**Modelli:**
- **XTTS v2:** MIT License ✅ Commerciale OK
- **Azzurra-voice:** CC-BY-NC ⚠️ Solo non commerciale
- **Resemble Chatterbox:** Apache 2.0 ✅ Commerciale OK

**Dataset:**
- **Common Voice:** CC0 (pubblico dominio) ✅ Commerciale OK
- **M-AILABS:** Varie licenze, controllare singolarmente

---

## 🎉 Changelog

### v1.0 (2025-01-12)
- ✅ Setup progetto iniziale
- ✅ Test Coqui XTTS v2 con voice cloning
- ✅ Download Azzurra-voice (13 file, ~5min)
- ✅ Conversione campione voce (MP4 → WAV 22050Hz)
- ✅ Generazione audio test 30 secondi
- ✅ Notebook Google Colab (3 versioni)
- ✅ Fix Python 3.12 compatibility
- ✅ Documentazione completa (5 guide MD)

---

## 🤝 Contributi

Contributi benvenuti! Per modifiche:
1. Fork repository
2. Crea branch (`git checkout -b feature/nuova-funzione`)
3. Commit (`git commit -m 'Aggiunta nuova funzione'`)
4. Push (`git push origin feature/nuova-funzione`)
5. Apri Pull Request

---

## 📧 Contatti

**Progetto:** SoloLabs SRL
**Repository:** https://github.com/sololabsrls-debug/Addestramento_Voce
**Issues:** https://github.com/sololabsrls-debug/Addestramento_Voce/issues

---

**Buon training! 🚀**
