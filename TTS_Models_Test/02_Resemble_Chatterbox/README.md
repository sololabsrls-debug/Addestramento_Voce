# Resemble Chatterbox - Italiano

## Caratteristiche
- **Licenza**: MIT License
- **Velocità**: Media-Veloce (RTF ~0.3-0.5)
- **Qualità**: Alta, buon bilanciamento
- **Modello**: Chatterbox 0.5B (multilingua)
- **Dimensione**: ~1 GB
- **GPU**: Consigliata
- **Particolarità**: Ottimo bilanciamento qualità/velocità/dimensione

## Installazione

```bash
chmod +x setup.sh
./setup.sh
```

## Generazione Audio

```bash
python3 generate.py
```

## Note
- Resemble Chatterbox è un modello 0.5B ottimizzato per efficienza
- Buon compromesso tra qualità e velocità
- Supporta multilingua incluso italiano
- Potrebbe richiedere accesso al repository HuggingFace
- Per accesso: `huggingface-cli login` con token HF

## Accesso HuggingFace
1. Crea account su huggingface.co
2. Richiedi accesso al modello resemble-ai/chatterbox
3. Genera token di accesso in Settings -> Access Tokens
4. Login: `huggingface-cli login`
5. Incolla il token quando richiesto

## Alternativa
Se Chatterbox non è accessibile, considera:
- **Coqui XTTS v2** - Qualità eccellente, versatile
- **Parler-TTS** - Controllo espressivo
- **Piper** - Leggero e veloce
