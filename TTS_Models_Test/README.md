# Test Modelli TTS Locali - Italiano

Questo progetto testa diversi modelli TTS open-source con licenza commerciale per l'italiano.

## 🎯 Quick Start

Per testare un modello:
```bash
cd [cartella_modello]
./setup.sh          # Installa il modello
python3 generate.py # Genera audio di test
```

L'audio generato sarà salvato come `output.wav` in ogni cartella.

## 📋 Modelli Testati (Solo Licenze Commerciali MIT/Apache 2.0)

### ⭐ Top 3 Consigliati per Uso Commerciale

1. **01_Piper** - MIT License ✅
   - ✓ Velocissimo (RTF < 0.1)
   - ✓ Leggero (~20 MB)
   - ✓ Non richiede GPU
   - ✓ Perfetto per assistenti telefonici real-time
   - ⚠️ Qualità buona ma non premium

2. **05_Parler_TTS** - Apache 2.0 ✅
   - ✓ Alta qualità
   - ✓ Controllo espressivo tramite descrizioni
   - ✓ Multilingua
   - ⚠️ Latenza media (RTF ~0.5-1.0)
   - ⚠️ Richiede GPU consigliata

3. **04_Bark** - MIT License ✅
   - ✓ Qualità eccellente ed espressiva
   - ✓ Può generare emozioni ed effetti sonori
   - ✓ Molto naturale
   - ⚠️ Lento (RTF ~1.5-2.0)
   - ⚠️ Richiede GPU consigliata

### Altri Modelli

4. **02_Resemble_Chatterbox** - MIT License ✅
   - Buon bilanciamento qualità/velocità
   - Modello 0.5B efficiente
   - Potrebbe richiedere accesso HuggingFace

5. **03_OpenVoice_v2** - MIT License ✅
   - Specializzato in voice cloning/conversion
   - Non genera audio da zero (richiede base audio)
   - Ottimo per tone color transfer

6. **06_Zonos** - Apache 2.0 ✅
   - Modello emergente, dialog-oriented
   - Potrebbe non essere ancora pubblicamente disponibile

### ⚠️ Modello NON per Uso Commerciale

7. **07_Coqui_XTTS** - MPL 2.0 ❌
   - ❌ Licenza MPL 2.0 con restrizioni commerciali
   - Qualità eccellente ma NON adatto per uso commerciale libero
   - Incluso solo per riferimento/test personale

## 📝 Testo di Test (30 secondi)

Tutti i modelli useranno lo stesso testo per confronto equo:

"Buongiorno, benvenuti nel nostro sistema di assistenza telefonica.
Sono un assistente virtuale e oggi vi parlerò della sintesi vocale in italiano.
La tecnologia text-to-speech permette di convertire il testo scritto in parlato naturale.
Questo modello è stato addestrato su migliaia di ore di audio in lingua italiana.
Posso gestire numeri come 12345, date come il 23 maggio 2025, e nomi propri come Milano e Bianchi.
La qualità della voce dipende dall'architettura del modello e dai dati di addestramento.
Grazie per l'ascolto, arrivederci!"

## 📁 Struttura Cartelle

```
TTS_Models_Test/
├── 01_Piper/                  # ✅ MIT - Veloce e leggero
├── 02_Resemble_Chatterbox/    # ✅ MIT - Bilanciamento qualità/velocità
├── 03_OpenVoice_v2/           # ✅ MIT - Voice cloning
├── 04_Bark/                   # ✅ MIT - Emotivo e creativo
├── 05_Parler_TTS/             # ✅ Apache 2.0 - Controllo espressivo
├── 06_Zonos/                  # ✅ Apache 2.0 - Dialog-oriented
└── 07_Coqui_XTTS/             # ❌ MPL 2.0 - NON commerciale
```

Ogni cartella contiene:
- `setup.sh` - Script di installazione
- `generate.py` - Script per generare audio
- `output.wav` - Audio generato (verrà creato)
- `README.md` - Note specifiche del modello

## 🎯 Caso d'Uso Consigliato (Solo Licenze Commerciali)

### Per Assistenti Telefonici (Real-Time)
→ **Piper** - Velocità massima, latenza minima, non richiede GPU

### Per Contenuti di Alta Qualità
→ **Bark** - Miglior qualità ed espressività (MIT License)
→ **Parler-TTS** - Alta qualità con controllo espressivo (Apache 2.0)

### Per Voice Cloning/Conversion
→ **OpenVoice v2** - Tone color transfer (MIT License)

### Per Contenuti Creativi/Narrativi
→ **Bark** - Espressività, emozioni ed effetti sonori (MIT License)

### Per Controllo Stile Vocale
→ **Parler-TTS** - Descrizioni testuali dello stile (Apache 2.0)

### Per Bilanciamento Qualità/Velocità
→ **Resemble Chatterbox** - Modello 0.5B efficiente (MIT License)

## ⚙️ Requisiti

### Minimo (CPU only)
- Python 3.8+
- 8 GB RAM
- Funzionano: Piper, Bark (lento), Parler-TTS (lento)

### Consigliato (GPU)
- Python 3.8+
- GPU NVIDIA con 4+ GB VRAM (es: RTX 3050 Ti)
- 16 GB RAM
- Tutti i modelli funzioneranno bene

## 🚀 Test Tutti i Modelli

Script per testare tutti i modelli automaticamente:

```bash
#!/bin/bash
for dir in */; do
    if [ -f "$dir/setup.sh" ]; then
        echo "Testing $dir..."
        cd "$dir"
        ./setup.sh
        python3 generate.py
        cd ..
        echo "---"
    fi
done
```

Salva come `test_all.sh` e esegui con `chmod +x test_all.sh && ./test_all.sh`

## 📊 Confronto Rapido - Solo Licenze Commerciali

### ✅ Modelli con Licenza Commerciale Pura (MIT/Apache 2.0)

| Modello | Licenza | Qualità | Velocità | GPU | Dimensione | Uso Commerciale |
|---------|---------|---------|----------|-----|------------|-----------------|
| **Piper** | MIT ✅ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | No | 20 MB | ✅ Sì |
| **Bark** | MIT ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐ | Consigliata | 2 GB | ✅ Sì |
| **Parler-TTS** | Apache 2.0 ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Consigliata | 1 GB | ✅ Sì |
| **Chatterbox** | MIT ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Consigliata | 1 GB | ✅ Sì |
| **OpenVoice v2** | MIT ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Consigliata | 300 MB | ✅ Sì |

### ❌ Modello NON per Uso Commerciale

| Modello | Licenza | Qualità | Velocità | GPU | Dimensione | Uso Commerciale |
|---------|---------|---------|----------|-----|------------|-----------------|
| Coqui XTTS | MPL 2.0 ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Sì | 2 GB | ❌ Limitato |

## 📚 Note Licenze

### ✅ Licenze Consigliate per Uso Commerciale

- **MIT License**: Uso commerciale completamente libero, minime restrizioni
  - Modelli: Piper, Bark, OpenVoice v2, Resemble Chatterbox

- **Apache 2.0**: Uso commerciale permesso, richiede attribution notice
  - Modelli: Parler-TTS, Zonos

### ⚠️ Licenze con Restrizioni

- **MPL 2.0 (Mozilla Public License)**: Uso commerciale con restrizioni
  - Modello: Coqui XTTS
  - ❌ Modifiche al codice devono rimanere open-source
  - ❌ Restrizioni per software proprietario
  - **NON CONSIGLIATO per uso commerciale**

### 🔍 Raccomandazione

Per uso commerciale sicuro, usa **SOLO modelli MIT o Apache 2.0**.

Verifica sempre i termini specifici di ogni modello prima dell'uso in produzione.
