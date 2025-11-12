# Coqui XTTS v2 - Italiano

## Caratteristiche
- **Licenza**: MPL 2.0 (Mozilla Public License) - Uso commerciale permesso
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
- XTTS v2 è uno dei migliori modelli per italiano
- Supporta voice cloning con solo 6 secondi di audio di riferimento
- Ottima prosodia e intonazione naturale
- Ideale per applicazioni professionali
- Richiede GPU per performance ottimali
- Uno dei modelli top consigliati per qualità/versatilità

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
