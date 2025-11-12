# 📦 Contenuto Cartella Colab_FineTuning

Tutto quello che ti serve per iniziare con il fine-tuning su Google Colab! 🚀

---

## ⚠️ IMPORTANTE - Python 3.12 su Colab

**Google Colab usa Python 3.12, ma TTS richiede Python ≤ 3.11**

**SOLUZIONE:** Leggi `SOLUZIONI_PYTHON312.md` per notebook aggiornati! 🔧

---

## 📂 Struttura Files

```
Colab_FineTuning/
├── SOLUZIONI_PYTHON312.md           ← ⚠️ LEGGI PRIMA! Risolve problema Python
├── XTTS_Colab_Alternativa.ipynb     ← ⚡ PROVA PRIMA (GitHub install, veloce)
├── XTTS_Colab_Python311.ipynb       ← 🐍 SOLUZIONE AFFIDABILE (conda + Python 3.11)
├── XTTS_Test_Semplice.ipynb         ← ❌ Non funziona (Python 3.12)
├── XTTS_FineTuning_Colab.ipynb      ← ❌ Non funziona (Python 3.12)
│
├── README.md                         ← Guida completa (aggiornare per Python 3.11)
├── QUICK_START.md                    ← Start veloce
├── INDEX.md                          ← Questo file
│
├── docs/
│   └── NOTE_TECNICHE.md              ← Approfondimenti tecnici
│
├── scripts/                          ← (vuota, per futuri script)
└── config/                           ← (vuota, per config custom)
```

---

## 🎯 Da Dove Iniziare? (AGGIORNATO 2025)

### **⚡ NUOVO UTENTE - Start Rapido (5 minuti)**
1. Leggi: `SOLUZIONI_PYTHON312.md`
2. Upload: `XTTS_Colab_Alternativa.ipynb` su Colab
3. Esegui celle in ordine!
4. Se fallisce → usa `XTTS_Colab_Python311.ipynb`

### **🎓 Vuoi capire tutto? (20 minuti)**
1. Leggi: `SOLUZIONI_PYTHON312.md` (problema Python)
2. Leggi: `README.md` (workflow completo)
3. Upload notebook corretto su Colab

### **🔬 Sei esperto e vuoi dettagli?**
1. Leggi: `SOLUZIONI_PYTHON312.md` (fix tecnico)
2. Leggi: `docs/NOTE_TECNICHE.md` (approfondimenti)
3. Scegli notebook basato su tue preferenze

---

## 📄 Descrizione Files

### 1️⃣ **XTTS_FineTuning_Colab.ipynb** ⭐ IMPORTANTE

**Cosa fa:**
- Download Common Voice italiano
- Preprocessing dataset (22.05kHz, normalizzato)
- Test voice cloning XTTS
- Salvataggio dataset preparato

**Quando usarlo:**
- Upload su Google Colab
- Esegui celle in ordine
- Ottieni dataset pronto

**Output:**
- `dataset_prepared.zip` (da scaricare!)
- Audio test voice cloning
- Metadata CSV

---

### 2️⃣ **README.md**

**Cosa contiene:**
- Guida completa step-by-step
- Setup Google Colab
- Troubleshooting
- FAQ
- Best practices

**Quando leggerlo:**
- Prima di iniziare (per capire flusso)
- Se hai problemi (troubleshooting)
- Per domande (FAQ)

**Sezioni:**
1. Setup iniziale
2. Upload notebook
3. Esecuzione
4. Download risultati
5. Troubleshooting
6. FAQ

---

### 3️⃣ **QUICK_START.md**

**Cosa contiene:**
- Start rapido 5 minuti
- 5 step essenziali
- No dettagli extra
- Solo azione

**Quando usarlo:**
- Sei esperto Colab
- Vuoi testare subito
- Hai poco tempo

**Tempo totale:** 10-30 minuti

---

### 4️⃣ **docs/NOTE_TECNICHE.md**

**Cosa contiene:**
- Architettura XTTS in dettaglio
- Confronto opzioni training
- Metriche valutazione
- Considerazioni produzione
- Paper e risorse

**Quando leggerlo:**
- Vuoi capire "perché"
- Progetti enterprise
- Ottimizzazioni avanzate
- Research/studio

**Pubblico:** Utenti avanzati, ML engineers

---

## 🎬 Workflow Consigliato

### **Step 1: Preparazione** (5-10 min)
1. Leggi `QUICK_START.md` o `README.md`
2. Vai su https://colab.research.google.com/
3. Upload `XTTS_FineTuning_Colab.ipynb`

### **Step 2: Esecuzione Colab** (10-30 min)
1. Attiva GPU (Runtime → GPU)
2. Esegui celle notebook in ordine
3. Wait for completion

### **Step 3: Download Risultati** (2 min)
1. Scarica `dataset_prepared.zip`
2. Scarica audio test
3. **Salva questi file!**

### **Step 4: Uso Locale** (immediato)
1. Usa dataset con XTTS locale
2. Voice cloning con tua voce
3. Production ready!

---

## 💡 Tips Utili

### **Per Principianti:**
- Inizia con `QUICK_START.md`
- Usa `num_samples=100` per test veloce
- Scarica sempre gli output prima di chiudere Colab

### **Per Utenti Intermedi:**
- Leggi `README.md` per capire opzioni
- Aumenta `num_samples=1000` per qualità
- Sperimenta con config diverse

### **Per Esperti:**
- Leggi `NOTE_TECNICHE.md`
- Modifica notebook per dataset custom
- Implementa fine-tuning completo (recipes Coqui)

---

## 🚀 Next Steps dopo Colab

### **Hai completato notebook. E ora?**

**Scenario A: Voice Cloning (RACCOMANDATO)**
```
Dataset preprocessato ✅
    ↓
Usa XTTS base localmente
    ↓
Voice cloning con tua voce (10s sample)
    ↓
Production ready! 🎉
```

**Scenario B: Fine-Tuning Vero (AVANZATO)**
```
Dataset preprocessato ✅
    ↓
Clone repo Coqui TTS
    ↓
Setup recipe XTTS custom
    ↓
10-20 ore training su Colab
    ↓
Download modello fine-tuned
    ↓
Usa localmente
```

**Scenario C: Alternativa VITS (INTERMEDIO)**
```
Dataset preprocessato ✅
    ↓
Clone repo VITS
    ↓
5-10 ore training
    ↓
Qualità 8/10
```

---

## 📊 Cosa Hai Dopo Colab

### **Files Scaricati:**
- ✅ `dataset_prepared.zip` (~500MB per 1000 samples)
  - Audio processati (22.05kHz WAV)
  - Metadata CSV
  - Pronto per training/inferenza

- ✅ `test_speaker_X.wav` (esempio output)
  - Test voice cloning
  - Valutazione qualità

### **Conoscenze Acquisite:**
- ✅ Come funziona preprocessing TTS
- ✅ Setup Google Colab con GPU
- ✅ Voice cloning XTTS
- ✅ Workflow ML audio

### **Pronto Per:**
- ✅ Produzione call center (voice cloning)
- ✅ Fine-tuning avanzato (se vuoi)
- ✅ Esperimenti custom

---

## 🆘 Help & Support

### **Hai problemi?**

**Ordine di consultazione:**
1. `QUICK_START.md` → Checklist base
2. `README.md` → Troubleshooting section
3. `docs/NOTE_TECNICHE.md` → Dettagli tecnici
4. Google Colab FAQ: https://research.google.com/colaboratory/faq.html

### **Errori Comuni:**

**"GPU not available"**
→ Runtime → Change runtime type → GPU

**"Out of memory"**
→ Riduci `num_samples` in config

**"Disconnected"**
→ Click nella pagina, evita timeout

**"File persi"**
→ Salva su Google Drive, non solo `/content/`

---

## 📚 Risorse Extra

**Documentazione:**
- Coqui TTS: https://github.com/coqui-ai/TTS
- Common Voice: https://commonvoice.mozilla.org/
- Hugging Face: https://huggingface.co/

**Community:**
- Coqui Discord: https://discord.gg/coqui
- r/MachineLearning: https://reddit.com/r/MachineLearning
- Hugging Face Forum: https://discuss.huggingface.co/

---

## ✅ Checklist Finale

Prima di iniziare, hai:
- [ ] Letto `QUICK_START.md` o `README.md`
- [ ] Account Google (Gmail)
- [ ] Browser aggiornato
- [ ] File `XTTS_FineTuning_Colab.ipynb` pronto

Dopo Colab, hai:
- [ ] Scaricato `dataset_prepared.zip`
- [ ] Salvato audio test
- [ ] Testato qualità voice cloning

Sei pronto per:
- [ ] Uso produzione (voice cloning)
- [ ] Fine-tuning avanzato (opzionale)
- [ ] Deploy call center

---

## 🎉 Buon Training!

Tutto chiaro? Inizia da:
→ `QUICK_START.md` (veloce)
→ `README.md` (dettagliato)

**Happy Coding! 🚀**
