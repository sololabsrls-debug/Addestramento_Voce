# ⚡ Quick Start - 5 Minuti

Vuoi iniziare **subito**? Segui questi 5 step! 🚀

---

## 📋 Checklist Pre-Partenza

- [ ] Account Google (Gmail)
- [ ] Browser Chrome/Firefox aggiornato
- [ ] File `XTTS_FineTuning_Colab.ipynb` scaricato

---

## 🎯 5 Step Rapidi

### **1️⃣ Apri Colab** (30 secondi)

```
https://colab.research.google.com/
```

Click: **"File" → "Upload notebook"**

Seleziona: `XTTS_FineTuning_Colab.ipynb`

---

### **2️⃣ Attiva GPU** (10 secondi)

```
Runtime → Change runtime type → GPU → Save
```

---

### **3️⃣ Esegui Setup** (2 minuti)

Click sulle prime 3 celle:
1. ✅ Verifica GPU
2. ✅ Install dependencies
3. ✅ Import librerie

Wait for completion (⏱️ ~2 min)

---

### **4️⃣ Configura & Run** (10-30 minuti)

**Cella 4 - Config:**
```python
"num_samples": 100,  # ← Inizia con 100 per test veloce
```

**Esegui celle 4-6:**
- Download Common Voice (5 min)
- Preprocessing (2 min)

---

### **5️⃣ Test & Download** (5 minuti)

**Esegui celle finali:**
- Test voice cloning
- Download dataset preparato

**Download file:**
```
dataset_prepared.zip  ← IMPORTANTE! Salva questo
test_speaker_0.wav    ← Ascolta qualità
```

---

## ✅ Fatto!

Ora hai:
- ✅ Dataset Common Voice IT preprocessato
- ✅ Test voice cloning funzionante
- ✅ Audio di esempio

---

## 🎯 Prossimo Step?

### **Opzione A: Usa Localmente** (RACCOMANDATO)

1. Scarica `dataset_prepared.zip`
2. Usa sul tuo PC con XTTS
3. Voice cloning con tua voce

### **Opzione B: Training Avanzato**

- Leggi `README.md` completo
- Setup training XTTS/VITS
- 10-20 ore training

### **Opzione C: Production Ready**

- Dataset ✅
- XTTS voice cloning ✅
- Deploy call center! 🎉

---

## ⚠️ Problemi Comuni

**"GPU not available":**
→ Runtime → Change runtime type → GPU

**"Out of memory":**
→ Riduci `num_samples` a 50

**"Disconnected":**
→ Click nella pagina ogni tanto

---

## 🆘 Aiuto?

- Leggi: `README.md` (completo)
- Troubleshooting: vedi sezione apposita
- FAQ: tutte le risposte comuni

---

**Buon divertimento! 🚀**
