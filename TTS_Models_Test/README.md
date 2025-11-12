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

## 📋 Modelli Testati

### ⭐ Top 3 Consigliati

1. **07_Coqui_XTTS** - MPL 2.0 License
   - ✓ Qualità eccellente, molto naturale
   - ✓ Voice cloning zero-shot
   - ✓ 17 lingue supportate
   - ⚠️ Richiede GPU (RTF ~0.8-1.2)
   - 📦 ~2 GB

2. **01_Piper** - MIT License
   - ✓ Velocissimo (RTF < 0.1)
   - ✓ Leggero (~20 MB)
   - ✓ Non richiede GPU
   - ⚠️ Qualità buona ma non premium

3. **05_Parler_TTS** - Apache 2.0
   - ✓ Alta qualità
   - ✓ Controllo espressivo
   - ✓ Multilingua
   - ⚠️ Latenza media (RTF ~0.5-1.0)

### Altri Modelli

4. **04_Bark** - MIT License
   - Emotivo e creativo, può generare effetti sonori
   - Lento (RTF ~1.5-2.0) ma molto espressivo

5. **03_OpenVoice_v2** - MIT License
   - Specializzato in voice cloning/conversion
   - Non genera audio da zero (richiede base audio)

6. **02_Resemble_Chatterbox** - MIT License
   - Buon bilanciamento qualità/velocità
   - Potrebbe richiedere accesso HuggingFace

7. **06_Zonos** - Apache 2.0
   - Modello emergente, dialog-oriented
   - Potrebbe non essere ancora pubblicamente disponibile

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
├── 01_Piper/                  # Veloce e leggero
├── 02_Resemble_Chatterbox/    # Bilanciamento qualità/velocità
├── 03_OpenVoice_v2/           # Voice cloning
├── 04_Bark/                   # Emotivo e creativo
├── 05_Parler_TTS/             # Controllo espressivo
├── 06_Zonos/                  # Dialog-oriented
└── 07_Coqui_XTTS/             # ⭐ Top qualità
```

Ogni cartella contiene:
- `setup.sh` - Script di installazione
- `generate.py` - Script per generare audio
- `output.wav` - Audio generato (verrà creato)
- `README.md` - Note specifiche del modello

## 🎯 Caso d'Uso Consigliato

### Per Assistenti Telefonici (Real-Time)
→ **Piper** - Velocità massima, latenza minima

### Per Contenuti di Alta Qualità
→ **Coqui XTTS v2** - Miglior qualità complessiva

### Per Voice Cloning
→ **Coqui XTTS v2** o **OpenVoice v2**

### Per Contenuti Creativi/Narrativi
→ **Bark** - Espressività ed emozioni

### Per Controllo Stile Vocale
→ **Parler-TTS** - Descrizioni testuali dello stile

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

## 📊 Confronto Rapido

| Modello | Licenza | Qualità | Velocità | GPU | Dimensione |
|---------|---------|---------|----------|-----|------------|
| Coqui XTTS | MPL 2.0 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Sì | 2 GB |
| Piper | MIT | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | No | 20 MB |
| Parler-TTS | Apache 2.0 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Consigliata | 1 GB |
| Bark | MIT | ⭐⭐⭐⭐⭐ | ⭐⭐ | Consigliata | 2 GB |
| Chatterbox | MIT | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Consigliata | 1 GB |
| OpenVoice v2 | MIT | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Consigliata | 300 MB |

## 📚 Note Licenze

Tutti i modelli qui testati hanno licenze compatibili con uso commerciale:
- **MIT License**: Uso commerciale permesso, minime restrizioni
- **Apache 2.0**: Uso commerciale permesso, richiede notice
- **MPL 2.0**: Uso commerciale permesso, modifiche devono rimanere open-source

Verifica sempre i termini specifici di ogni modello prima dell'uso in produzione.
