# 🎙️ Piper TTS - Training & Fine-Tuning

Progetto per training e fine-tuning di modelli Piper TTS con voci personalizzate.

## 🚀 Quick Start

Scegli il percorso più adatto a te:

### **Percorso 1: Fine-Tuning Veloce** ⚡ (Raccomandato per iniziare)

Adatta un modello esistente con il tuo dataset (30+ minuti di audio).

1. **Apri:** `piper_training/Piper_FineTuning_Colab.ipynb`
2. **Upload su Colab:** https://colab.research.google.com
3. **Attiva GPU:** Runtime → Change runtime type → GPU (T4)
4. **Esegui:** Run all
5. **Tempo:** ~8-12 ore

### **Percorso 2: Training Completo** 🎯 (Per massima qualità)

Addestra un modello da zero (2+ ore di audio consigliato).

1. **Apri:** `piper_training/Piper_Training_Complete.ipynb`
2. **Upload su Colab:** https://colab.research.google.com
3. **Attiva GPU:** Runtime → Change runtime type → GPU (T4)
4. **Esegui:** Run all
5. **Tempo:** ~12-16 ore

### **Guide Disponibili**

- 📖 **Guida Completa:** `piper_training/PIPER_TRAINING_GUIDE.md` - Tutto quello che devi sapere
- ⚡ **Quick Start:** `piper_training/PIPER_QUICK_START.md` - Inizia in 2 passi

## 📊 Dataset

Il notebook utilizza il dataset **LJSpeech-IT** (giacomoarienti/female-LJSpeech-italian):
- **5,856 campioni audio**
- **~10-11 ore** di parlato
- **Voce femminile** italiana
- **Qualità media-alta**

## 🎯 Modelli Piper

Piper supporta diverse qualità di modelli:
- **x_low**: Qualità bassa, veloce
- **low**: Qualità medio-bassa
- **medium**: Qualità media (consigliato)
- **high**: Qualità alta (richiede più risorse)

## 📁 Struttura Progetto

```
Addestramento_Voce/
├── piper_training/                           # 📁 Tutto per il training
│   ├── Piper_FineTuning_Colab.ipynb         # Fine-tuning veloce (8-12h)
│   ├── Piper_Training_Complete.ipynb        # Training completo (12-16h)
│   ├── PIPER_TRAINING_GUIDE.md              # Guida completa con troubleshooting
│   └── PIPER_QUICK_START.md                 # Quick start 2-step
├── piper/                                    # Binari Piper (generati)
├── scripts/                                  # Script utility
├── README.md                                 # Questa guida
└── requirements.txt                          # Dipendenze Python
```

## 💻 Uso Locale (Opzionale)

Se vuoi usare Piper localmente dopo il training:

### Installazione

```bash
# Download Piper (Windows)
wget https://github.com/rhasspy/piper/releases/latest/download/piper_windows_amd64.zip
unzip piper_windows_amd64.zip

# Linux/Mac
wget https://github.com/rhasspy/piper/releases/latest/download/piper_amd64.tar.gz
tar -xzf piper_amd64.tar.gz
```

### Generazione Audio

```bash
# Con il tuo modello custom
echo "Questo è un test" | ./piper/piper \
  --model ./tuo_modello.onnx \
  --output_file output.wav
```

## 🔧 Requisiti

### Per Colab (Consigliato):
- Google account
- GPU T4 (gratis su Colab)
- ~10GB spazio Drive

### Per Training Locale:
- Python 3.9-3.11
- GPU NVIDIA con CUDA (24GB VRAM consigliati)
- PyTorch
- `piper_train` package

## 📖 Risorse

- **Piper TTS**: https://github.com/rhasspy/piper
- **Piper Training Docs**: https://github.com/rhasspy/piper/blob/master/TRAINING.md
- **Dataset LJSpeech-IT**: https://huggingface.co/datasets/giacomoarienti/female-LJSpeech-italian
- **Modelli Pre-addestrati**: https://huggingface.co/rhasspy/piper-voices

## ⚙️ Parametri Training Consigliati

```python
# Fine-tuning (da modello esistente)
MAX_EPOCHS = 1000
BATCH_SIZE = 8  # Riduci se OOM
QUALITY = "medium"
SAMPLE_RATE = 22050

# Training da zero (non consigliato senza dataset grande)
MAX_EPOCHS = 2000
DATASET_SIZE = "13,000+ campioni"
```

## 🎓 Processo Fine-Tuning

1. **Preprocessing** (~10-30 min)
   - Download dataset
   - Conversione audio in formato corretto
   - Generazione phonemi con espeak-ng

2. **Training** (~8-12 ore per fine-tuning)
   - Caricamento checkpoint base
   - Training con GPU T4
   - Salvataggio checkpoints ogni 100 epoch

3. **Export** (~5 min)
   - Conversione checkpoint → ONNX
   - Generazione config.json
   - Test audio

4. **Download** (~2 min)
   - Download modello.onnx
   - Download modello.onnx.json
   - Pronto per l'uso!

## 📝 Note

- **Colab Free**: Limite 12 ore → Usa checkpoints per riprendere
- **Colab Pro** (€10/mese): 24 ore, GPU migliori
- **Real-Time Factor**: Piper è molto veloce (~0.1 RTF = 10x real-time)
- **Qualità**: Fine-tuning produce risultati migliori di training da zero con dataset piccoli

## 🐛 Troubleshooting

### Out of Memory su Colab
```python
# Riduci batch size nel notebook
BATCH_SIZE = 4  # invece di 8
```

### Training troppo lento
```python
# Verifica GPU attiva
import torch
print(torch.cuda.is_available())  # Deve essere True
```

### Modello finale robotico
- Aumenta epoch di training
- Verifica qualità dataset (audio pulito?)
- Prova fine-tuning invece di training da zero

## 📄 Licenza

Questo progetto: MIT License

**Modelli e Dataset:**
- Piper TTS: MIT License ✅ Commerciale OK
- LJSpeech-IT: Apache 2.0 ✅ Commerciale OK

---

## 🎉 Credits

- **Piper TTS**: https://github.com/rhasspy/piper (Rhasspy team)
- **LJSpeech-IT Dataset**: giacomoarienti (Hugging Face)
- **Training Framework**: PyTorch + Lightning

---

**Buon fine-tuning! 🚀**
