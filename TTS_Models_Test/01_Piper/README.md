# Piper TTS - Italiano

## Caratteristiche
- **Licenza**: MIT License
- **Velocità**: Molto veloce (RTF < 0.1)
- **Qualità**: Buona per uso generale
- **Modello**: it_IT-riccardo-x_low (ONNX)
- **Dimensione**: ~20 MB
- **GPU**: Non richiesta

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
- Piper utilizza modelli ONNX molto leggeri
- Ottimo per applicazioni real-time
- Voce naturale ma meno espressiva di modelli più grandi
- Ideale per sistemi con risorse limitate
