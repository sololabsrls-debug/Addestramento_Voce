# Parler-TTS - Italiano

## Caratteristiche
- **Licenza**: Apache 2.0
- **Velocità**: Media (RTF ~0.5-1.0)
- **Qualità**: Alta, molto naturale
- **Modello**: parler-tts-mini-v1 (multilingua)
- **Dimensione**: ~1 GB
- **GPU**: Consigliata (funziona su CPU ma più lento)
- **Particolarità**: Controllo espressivo tramite descrizione testuale

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
- Parler-TTS permette di controllare lo stile vocale tramite descrizioni testuali
- Supporta multilingua incluso italiano
- Ottima qualità con latenza accettabile
- Puoi modificare la descrizione della voce in generate.py per cambiare stile
- Esempi di descrizioni: "energetic", "calm", "professional", "friendly"
