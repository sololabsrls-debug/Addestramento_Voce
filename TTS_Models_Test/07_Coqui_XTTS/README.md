# Coqui XTTS v2 - Italiano

## ⚠️ ATTENZIONE - Licenza NON Commerciale

**Licenza**: MPL 2.0 (Mozilla Public License) - ❌ **NON ADATTO per uso commerciale libero**

### Restrizioni MPL 2.0:
- ❌ Modifiche al codice devono rimanere open-source
- ❌ Restrizioni per software proprietario
- ⚠️ Non è completamente libero come MIT o Apache 2.0

### 🔍 Raccomandazione:
**Per uso commerciale, usa invece:**
- **Bark** (MIT) - Qualità eccellente, emotivo
- **Parler-TTS** (Apache 2.0) - Alta qualità con controllo espressivo
- **Piper** (MIT) - Veloce e affidabile

---

## Caratteristiche Tecniche
- **Licenza**: MPL 2.0 ❌
- **Velocità**: Media (RTF ~0.8-1.2)
- **Qualità**: Eccellente, molto naturale
- **Modello**: XTTS v2 multilingua
- **Dimensione**: ~2 GB
- **GPU**: Consigliata (RTX 3050 Ti o superiore)
- **Particolarità**: Supporta voice cloning zero-shot e 17 lingue

## Installazione

```bash
chmod +x setup.sh
./setup.sh
```

## Generazione Audio

```bash
python3 generate.py
```

L'audio verrà salvato in `output.wav`.

## Note

### ⚠️ IMPORTANTE
- **Questo modello NON è consigliato per uso commerciale** a causa della licenza MPL 2.0
- Incluso solo per test e riferimento personale
- Per uso commerciale, scegli modelli MIT o Apache 2.0

### Caratteristiche Tecniche
- XTTS v2 è uno dei migliori modelli per qualità
- Supporta voice cloning con solo 6 secondi di audio di riferimento
- Ottima prosodia e intonazione naturale
- Richiede GPU per performance ottimali

### Alternative Commerciali Consigliate
- **Bark** (MIT) - Qualità paragonabile, completamente commerciale
- **Parler-TTS** (Apache 2.0) - Alta qualità, controllo espressivo
- **Piper** (MIT) - Veloce e affidabile per real-time

## Voice Cloning (Opzionale)
Per usare il voice cloning, aggiungi al file generate.py:
```python
tts.tts_to_file(
    text=TEST_TEXT,
    language="it",
    speaker_wav="path/to/reference_audio.wav",  # 6+ secondi di audio
    file_path=output_path
)
```
