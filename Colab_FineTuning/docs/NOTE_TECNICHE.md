# 📝 Note Tecniche - Fine-Tuning TTS

Informazioni avanzate per chi vuole approfondire.

---

## 🎓 Perché Fine-Tuning Completo XTTS è Complesso

### **Architettura XTTS v2:**

XTTS è composto da **3 modelli** separati:

1. **GPT Encoder** (~1B parametri)
   - Converte testo in embedding semantici
   - Pre-trained su 16 lingue

2. **DVAE (Discrete VAE)** (~500M parametri)
   - Converte audio in codebook tokens
   - Compressione audio

3. **Diffusion Decoder** (~500M parametri)
   - Genera audio da tokens
   - Condizionato su speaker embedding

**Totale:** ~2B parametri

### **Perché è Difficile:**

**1. Setup Complesso:**
- Serve repo Coqui TTS completo
- Config files custom per ogni dataset
- Multiple training stages
- Checkpointing avanzato

**2. Risorse GPU:**
- Training: 16-24GB VRAM minimo
- Batch size piccolo su T4 (16GB)
- 10-20 ore training minimo

**3. Dataset Requirements:**
- Minimo 5-10 ore audio
- Meglio 20-50 ore
- Metadata accurati
- Speaker ID consistency

---

## 🔬 Alternative Pratiche

### **Opzione 1: Voice Cloning (Zero Training)**

**Come funziona:**
```
XTTS pre-trained + 10s voice sample → Cloned voice
```

**Pro:**
- ✅ Zero training time
- ✅ Funziona subito
- ✅ Qualità 9/10
- ✅ Flessibile (cambi voce quando vuoi)

**Contro:**
- ⚠️ Pronuncia dipende da pre-training
- ⚠️ Alcuni termini tecnici potrebbero essere imperfetti

**Quando usarlo:**
- Call center standard
- Progetti rapidi
- Budget/tempo limitato
- **90% dei casi!**

---

### **Opzione 2: Adapter Training (Compromesso)**

**Cosa sono gli Adapter:**
- Piccoli layer addizionali (5-10M parametri)
- Si aggiungono a modello frozen
- Training molto più veloce

**Setup:**
```python
# Freeze base model
for param in model.parameters():
    param.requires_grad = False

# Add adapter layers
model.add_adapter("italian_adapter", adapter_size=64)

# Train only adapter
optimizer = Adam(model.adapter_parameters(), lr=1e-4)
```

**Pro:**
- ✅ Training 10x più veloce
- ✅ Serve meno VRAM (8-12GB)
- ✅ Migliora pronuncia specifica
- ✅ Mantiene capacità generale

**Contro:**
- ⚠️ Miglioramento limitato vs full fine-tune
- ⚠️ Setup comunque tecnico

**Quando usarlo:**
- Termini tecnici specifici (medico, legale)
- Accento particolare
- Budget/tempo medio

---

### **Opzione 3: Full Fine-Tuning**

**Setup Completo:**

**Step 1: Clone Coqui TTS**
```bash
git clone https://github.com/coqui-ai/TTS
cd TTS
pip install -e .
```

**Step 2: Prepara Config**
```python
# config.json per XTTS
{
    "model": "xtts_v2",
    "run_name": "xtts_italian",
    "datasets": [{
        "formatter": "common_voice",
        "path": "/path/to/common_voice_it/",
        "language": "it"
    }],
    "audio": {
        "sample_rate": 22050,
        "max_audio_length": 11.0
    },
    "batch_size": 2,
    "num_epochs": 1000,
    "learning_rate": 1e-5,
    "checkpoint_path": "/path/to/xtts_base"
}
```

**Step 3: Training**
```bash
python TTS/bin/train_xtts.py \
    --config_path config.json \
    --restore_path models/xtts_v2.pth
```

**Pro:**
- ✅ Massima qualità possibile
- ✅ Controllo completo
- ✅ Pronuncia perfetta

**Contro:**
- ❌ Setup complesso
- ❌ 10-20 ore training
- ❌ Richiede esperienza ML
- ❌ Debug difficile

**Quando usarlo:**
- Prodotto enterprise critico
- Hai team ML dedicato
- Budget tempo/GPU alto
- Serve qualità assoluta

---

## 📊 Confronto Opzioni

| Aspetto | Voice Cloning | Adapter | Full Fine-Tune |
|---------|---------------|---------|----------------|
| **Setup Time** | 5 min | 1-2 ore | 1-2 giorni |
| **Training Time** | 0 | 2-4 ore | 10-20 ore |
| **VRAM Required** | 4GB (inference) | 8-12GB | 16-24GB |
| **Qualità Finale** | 9/10 | 9.5/10 | 9.8/10 |
| **Flessibilità** | Alta | Media | Bassa |
| **Complessità** | Facile | Media | Alta |
| **Costo GPU Colab** | $0 | ~$2-5 | ~$10-20 |
| **Uso Commerciale** | ✅ | ✅ | ✅ |
| **Raccomandato Per** | 90% casi | Casi specifici | Enterprise |

---

## 🎯 Metriche di Valutazione

### **Come Misurare Qualità TTS:**

**1. MOS (Mean Opinion Score)**
- Soggettivo: persone votano 1-5
- Gold standard industria
- Costoso (serve panel tester)

**2. WER (Word Error Rate)**
- Oggettivo: ASR riconosce testo
- WER basso = pronuncia chiara
- Facile automatizzare

**3. MCD (Mel Cepstral Distortion)**
- Misura distanza spettrale
- Audio generato vs reference
- Correlazione con qualità percepita

**4. RTF (Real-Time Factor)**
- Velocità sintesi
- RTF < 1.0 = più veloce del tempo reale
- Critico per produzione

### **Testing Pratico:**

```python
# Test WER
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import librosa

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-it")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-it")

# Load generated audio
audio, sr = librosa.load("generated.wav", sr=16000)

# ASR transcription
inputs = processor(audio, sampling_rate=sr, return_tensors="pt")
predicted_ids = model(**inputs).logits.argmax(-1)
transcription = processor.decode(predicted_ids[0])

# Compare with original text
from jiwer import wer
error_rate = wer(original_text, transcription)
print(f"WER: {error_rate:.2%}")
```

---

## 💾 Storage & Bandwidth

### **Dataset Sizes:**

| Dataset | Audio | Storage | Download Time |
|---------|-------|---------|---------------|
| CV IT (100 samples) | ~10 min | ~50 MB | 1 min |
| CV IT (1000 samples) | ~1.5 ore | ~500 MB | 5 min |
| CV IT (full) | ~150 ore | ~50 GB | 1-2 ore |

### **Model Sizes:**

| Modello | Parametri | Storage |
|---------|-----------|---------|
| XTTS v2 | 2B | ~4 GB |
| VITS | 100M | ~400 MB |
| Tacotron 2 | 50M | ~200 MB |
| Piper | 20M | ~80 MB |

### **Colab Storage:**

- `/content/`: ~100GB temp (perso a fine sessione)
- Google Drive: 15GB free (persistente)
- **Tip:** Compress dataset prima di salvare

---

## 🔐 Sicurezza & Privacy

### **Common Voice Dataset:**

- ✅ Audio sono **pubblici** (volontari consenso)
- ✅ Licenza CC0 (pubblico dominio)
- ✅ Nessun dato sensibile
- ✅ OK per produzione commerciale

### **Dati Custom:**

**Se registri propri audio:**

**Consenso necessario:**
- ✅ Tua voce: OK
- ⚠️ Dipendenti: serve consenso scritto
- ❌ Clienti: NO senza consenso esplicito
- ❌ Celebrità: NO (diritti immagine)

**GDPR Compliance:**
- Voce = dato biometrico
- Serve:
  - Consenso esplicito
  - Informativa privacy
  - Diritto cancellazione
  - Storage sicuro

**Best Practice:**
```
1. Consenso scritto da speaker
2. Anonimizza speaker ID
3. Storage encrypted
4. Access control
5. Audit log
```

---

## 🌍 Multi-lingua vs Single-lingua

### **XTTS Multi-lingua (16 lingue):**

**Pro:**
- Transfer learning tra lingue
- Pronuncia straniera migliore
- Flessibilità

**Contro:**
- Pronuncia italiano non perfetta
- Mixing accidentale lingue

### **Modello Single-lingua (solo IT):**

**Pro:**
- Pronuncia italiana perfetta
- Accenti regionali migliori
- Meno confusione

**Contro:**
- Meno flessibile
- Richiede training from scratch
- Nomi stranieri problematici

### **Soluzione Ibrida:**

```
XTTS multi-lingua (base)
    ↓
Fine-tune su IT
    ↓
Mantiene: capacità generale + nomi stranieri
Migliora: pronuncia italiana, prosodia
```

---

## 🔬 Research vs Production

### **Per Ricerca/Esperimenti:**

- Qualità > Velocità
- Test hyperparameters
- Modelli grandi OK
- RTF non critico

### **Per Produzione (Call Center):**

**Requisiti:**
- ✅ RTF < 1.0 (preferibile < 0.5)
- ✅ Qualità consistente
- ✅ Latenza bassa (<2s end-to-end)
- ✅ Affidabilità 99.9%
- ✅ Scalabilità (100+ chiamate simultanee)

**Ottimizzazioni:**
```python
# Quantizzazione (FP16)
model.half()  # ~50% più veloce, -1% qualità

# Compiled model (PyTorch 2.0)
model = torch.compile(model)  # +20-30% velocità

# Batch processing (se possibile)
batch_size = 8  # Processa più richieste insieme

# Caching
# Cache frasi comuni pre-generate
```

---

## 📚 Risorse Avanzate

### **Papers Chiave:**

**XTTS:**
- "Massively Multilingual Speech (MMS)" (Meta, 2023)
- GPT-based TTS architecture

**VITS:**
- "Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech" (2021)
- Current SOTA architecture

**General TTS:**
- Tacotron 2 (Google, 2017)
- FastSpeech 2 (2020)
- VALL-E (Microsoft, 2023)

### **Repositories:**

- Coqui TTS: https://github.com/coqui-ai/TTS
- VITS: https://github.com/jaywalnut310/vits
- SpeechBrain: https://github.com/speechbrain/speechbrain

### **Datasets Italian:**

- Common Voice: https://commonvoice.mozilla.org/
- VoxPopuli: https://github.com/facebookresearch/voxpopuli
- M-AILABS: https://www.caito.de/2019/01/the-m-ailabs-speech-dataset/

---

**Buono studio! 📚**
